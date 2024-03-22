from rest_framework_simplejwt.authentication import JWTAuthentication
from dev_JUN.models import User
from common.response_codes import *
from common.common_exceptions import *

"""
@date 2024-02-16
@updated 2024-02-16
@author 정준이
@description JWT 인증 Authentication 클래스
"""
class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            raise SingleMessageError(JWT_ATTRIBUTE_NOT_EXIST) # 토큰을 담는 항목이 없음

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            raise SingleMessageError(JWT_NOT_EXIST) # 토큰이 없음

        # get_validated_token 을 통해 JWT 검증
        try:
            validated_token = self.get_validated_token(raw_token)
        except Exception as e:
            raise SingleMessageError(JWT_INVALID)

        user_id = validated_token['uid']
        try:
            user = User.objects.get(uid=user_id)
        except User.DoesNotExist:
            raise SingleMessageError(USER_NOT_EXIST)
        print("??")
        return (user, None)