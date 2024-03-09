#!/bin/bash

# Replaces submodules GitLab URL with GitHub URL and creates a backup file
# ssh://git@gitlab.internal.lan:2222/octo-project/<repo>.git becomes ssh://git@github.com:nillyr/<repo>.git
sed -i.bak 's/gitlab.internal.lan:2222\/octo-project/github.com:nillyr/g' .gitmodules
