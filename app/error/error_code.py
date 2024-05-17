from app.error import APIException


class Success(APIException):
    code = 200
    msg = "success"
    error_code = 0


class ParameterException(APIException):
    code = 200
    msg = 'invalid parameter'
    error_code = 101


class ServerError(APIException):
    code = 500
    msg = 'server is busy!'
    error_code = 1000
