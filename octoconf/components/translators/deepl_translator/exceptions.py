# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0


class BaseException(Exception):
    def __init__(self, error_code: str, error_message: str) -> None:
        self._error_code = error_code
        self._error_message = error_message
        super().__init__()

    def __str__(self) -> str:
        return f"{self._error_code}: {self._error_message}"


class DeepLError(BaseException):
    """
    Implementation of the errors defined in the DeepL documentation.

    See also: https://www.deepl.com/fr/docs-api/accessing-the-api/error-handling/
    """

    _errors = {
        400: {
            "error_code": "DEEPL_ERR_BAD_REQUEST",
            "error_message": "Please check error message and your parameters.",
        },
        403: {
            "error_code": "DEEPL_ERR_AUTHORIZATION_FAILED",
            "error_message": "Please supply a valid auth_key parameter.",
        },
        404: {
            "error_code": "DEEPL_ERR_REQUESTED_RESOURCE_NOT_FOUND",
            "error_message": "The requested resource could not be found.",
        },
        413: {
            "error_code": "DEEPL_ERR_SIZE_LIMT_EXCEEDED",
            "error_message": "The request size exceeds the limit.",
        },
        414: {
            "error_code": "DEEPL_ERR_URL_TOO_LONG",
            "error_message": "The request URL is too long.",
        },
        429: {
            "error_code": "DEEPL_ERR_TOO_MANY_REQUESTS",
            "error_message": "Please wait and resend your request.",
        },
        456: {
            "error_code": "DEEPL_ERR_QUOTA_EXCEEDED",
            "error_message": "The character limit has been reached.",
        },
        503: {
            "error_code": "DEEPL_ERR_RESOURCE_UNAVAILABLE",
            "error_message": "Resource currently unavailable. Try again later.",
        },
        529: {
            "error_code": "DEEPL_ERR_TOO_MANY_REQUESTS",
            "error_message": "Please wait and resend your request.",
        },
    }

    def __init__(self, status_code: int, server_response_message: str) -> None:
        error_code = self._errors[status_code].get("error_code")
        error_message = (
            self._errors[status_code].get("error_message")
            + " (info: "
            + server_response_message
            + ")"
        )
        super(DeepLError, self).__init__(error_code, error_message)
