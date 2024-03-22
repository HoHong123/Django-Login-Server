from rest_framework.exceptions import APIException
from .response_codes import *

"""
@date 2024-02-08
@author 정준이
@description 단순 객체 1개(detail) 만을 담는 에러 - rest_framework.exceptions.APIException 기반
"""
class SingleMessageError(APIException):
    def __init__(self, errorCode):
        self.detail = errorCode