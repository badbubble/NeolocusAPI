from werkzeug.exceptions import HTTPException
from typing import Optional, Any
from flask import request, json


class APIException(HTTPException):
    # default variables
    code = 500
    description = 'An unexpected error has occurred.'
    error_code = 1000

    def __init__(
            self,
            msg: dict[str | None, Any] = None,
            code: dict[int | None, Any] = None,
            error_code: dict[int | None, Any] = None,
            headers: dict[dict | None, Any] = None
    ) -> None:

        if msg is not None:
            self.msg = msg

        if code is not None:
            self.code = code

        if error_code is not None:
            self.error_code = error_code

        super(APIException, self).__init__(msg, code)

    def get_body(self, environ: Any = None, scope: Any = None) -> str:
        body = dict(
            msg=self.msg,
            error_code=self.error_code,
            request=request.method + ' ' + self.get_url_no_param()
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ: Optional[Any] = None, scope: Optional[Any] = None) -> list[tuple[str, str]]:
        """Get a list of headers."""
        return [("Content-Type", "text/html; charset=utf-8")]

    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]
