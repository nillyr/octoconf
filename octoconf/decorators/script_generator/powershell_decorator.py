# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

from octoconf.decorators.decorator import Decorator


class PowershellDecorator(Decorator):
    """
    It allows to add instructions before and after the execution of the commands. Among these instructions are the verification of the user's privileges, the creation of the working folder and the creation of the archive.
    """

    def decorator(func):
        def inner(*args, **kwargs):
            content = []
            prolog = """# Prolog
#Requires -RunAsAdministrator
#Requires -version 2

if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Error "[x] Error: This script is meant to be run with administrator rights"
    exit
}

Write-Output "[*] Preparation..."
$basedir = "$pwd\Audit_$($env:COMPUTERNAME)_$(get-date -f yyyyMMdd-hhmmss)"
New-Item -ItemType Directory -Force -Path $basedir | Out-Null
$system_information_dir = "$basedir\\00_system_information"
New-Item -ItemType Directory -Force -Path $system_information_dir | Out-Null
$checksdir = "$basedir\\10_octoconf_checks"
New-Item -ItemType Directory -Force -Path $checksdir | Out-Null

date >> $system_information_dir\\timestamp.txt
[System.Net.Dns]::GetHostName() >> $system_information_dir\\hostname.txt
(Get-CimInstance Win32_OperatingSystem).Caption >> $system_information_dir\\os.txt
(Get-CimInstance Win32_OperatingSystem).Version >> $system_information_dir\\os_version.txt
Get-ChildItem -Path Env: | Format-Table -AutoSize >> $system_information_dir\\env.txt
whoami /all >> $system_information_dir\\whoami.txt

# Custom functions
$custom_functions_dir = "$basedir\\20_custom_functions"
New-Item -ItemType Directory -Force -Path $custom_functions_dir | Out-Null

Function Test-CommandExists {
	Param ($command)
	$oldPreference = $ErrorActionPreference
	$ErrorActionPreference = "Stop"
	try {
		If (Get-Command $command) {
			return $true
		}
	} Catch {
		return $false
	} Finally {
		$ErrorActionPreference = $oldPreference
	}
}

function _collect_user_rights_assigments {
    # Fail script if we can't find SecEdit.exe
    $SecEdit = Join-Path ([Environment]::GetFolderPath([Environment+SpecialFolder]::System)) "SecEdit.exe"
    if ( -not (Test-Path $SecEdit) ) {
        Write-Error "File not found - '$SecEdit'" -Category ObjectNotFound
        exit
    }

    # LookupPrivilegeDisplayName Win32 API doesn't resolve logon right display
    # names, so use this hashtable
    $UserLogonRights = @{
        "SeBatchLogonRight"                 = "Log on as a batch job"
        "SeDenyBatchLogonRight"             = "Deny log on as a batch job"
        "SeDenyInteractiveLogonRight"       = "Deny log on locally"
        "SeDenyNetworkLogonRight"           = "Deny access to this computer from the network"
        "SeDenyRemoteInteractiveLogonRight" = "Deny log on through Remote Desktop Services"
        "SeDenyServiceLogonRight"           = "Deny log on as a service"
        "SeInteractiveLogonRight"           = "Allow log on locally"
        "SeNetworkLogonRight"               = "Access this computer from the network"
        "SeRemoteInteractiveLogonRight"     = "Allow log on through Remote Desktop Services"
        "SeServiceLogonRight"               = "Log on as a service"
    }

    # Create type to invoke LookupPrivilegeDisplayName Win32 API
    $Win32APISignature = @'
[DllImport("advapi32.dll", SetLastError=true)]
public static extern bool LookupPrivilegeDisplayName(
  string systemName,
  string privilegeName,
  System.Text.StringBuilder displayName,
  ref uint cbDisplayName,
  out uint languageId
);
'@
    $AdvApi32 = Add-Type advapi32 $Win32APISignature -Namespace LookupPrivilegeDisplayName -PassThru

    # Use LookupPrivilegeDisplayName Win32 API to get display name of privilege
    # (except for user logon rights)
    function Get-PrivilegeDisplayName {
        param(
            [String] $name
        )
        $displayNameSB = New-Object System.Text.StringBuilder 1024
        $languageId = 0
        $ok = $AdvApi32::LookupPrivilegeDisplayName($null, $name, $displayNameSB, [Ref] $displayNameSB.Capacity, [Ref] $languageId)
        if ( $ok ) {
            $displayNameSB.ToString()
        }
        else {
            # Doesn't lookup logon rights, so use hashtable for that
            if ( $UserLogonRights[$name] ) {
                $UserLogonRights[$name]
            }
            else {
                $name
            }
        }
    }

    # Outputs list of hashtables as a PSObject
    function Out-Object {
        param(
            [System.Collections.Hashtable[]] $hashData
        )
        $order = @()
        $result = @{ }
        $hashData | ForEach-Object {
            $order += ($_.Keys -as [Array])[0]
            $result += $_
        }
        New-Object PSObject -Property $result | Select-Object $order
    }

    # Translates a SID in the form *S-1-5-... to its account name
    function Get-AccountName {
        param(
            [String] $principal
        )
        if ( $principal[0] -eq "*" ) {
            $sid = New-Object System.Security.Principal.SecurityIdentifier($principal.Substring(1))
            $sid.Translate([Security.Principal.NTAccount])
        }
        else {
            $principal
        }
    }

    $TemplateFilename = Join-Path ([IO.Path]::GetTempPath()) ([IO.Path]::GetRandomFileName())
    $LogFilename = Join-Path ([IO.Path]::GetTempPath()) ([IO.Path]::GetRandomFileName())
    $StdOut = & $SecEdit /export /cfg $TemplateFilename /areas USER_RIGHTS /log $LogFilename
    if ( $LASTEXITCODE -eq 0 ) {
        Select-String '^(Se\S+) = (\S+)' $TemplateFilename | Foreach-Object {
            $Privilege = $_.Matches[0].Groups[1].Value
            $Principals = $_.Matches[0].Groups[2].Value -split ','
            foreach ( $Principal in $Principals ) {
                Out-Object `
                @{"Privilege" = $Privilege },
                @{"PrivilegeName" = Get-PrivilegeDisplayName $Privilege },
                @{"Principal" = Get-AccountName $Principal }
            }
        }
    }
    else {
        $OFS = ""
        Write-Error "$StdOut"
    }
    Remove-Item $TemplateFilename, $LogFilename -ErrorAction SilentlyContinue

}

_collect_user_rights_assigments | Format-Table -AutoSize -Wrap | Out-File -Encoding utf8 -Append -FilePath $custom_functions_dir\\collect_user_rights_assigments.txt

# Configuration collection
Write-Output "[*] Beginning of the collection..."
"""
            content.append(prolog)
            content.extend(func(*args, **kwargs))
            epilog = """# Epilog
Write-Output "[*] Finishing..."
date >> $system_information_dir\\timestamp.txt
try {
    Get-Command Compress-Archive | Out-Null
    Compress-Archive -Path ($basedir) -DestinationPath "$($basedir).zip"
    Write-Output "[+] Archive created!"
} catch {
    Write-Error "[x] Compress-Archive command not found!"
}
Write-Output "[+] Done!"
"""
            content.append(epilog)
            return content

        return inner
