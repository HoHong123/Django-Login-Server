from rest_framework_simplejwt.authentication import JWTAuthentication
from API.models import User
from common.response_codes import *
from common.common_exceptions import *

from HWS.settings.base import BASE_LOGGER
import logging

logger = logging.getLogger(BASE_LOGGER)

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
            logger.error(f'CustomJWTAuthentication header not found({request})')
            raise SingleMessageError(JWT_ATTRIBUTE_NOT_EXIST) # 토큰을 담는 항목이 없음

        rawToken = self.get_raw_token(header)
        if rawToken is None:
            logger.error(f'CustomJWTAuthentication rawToken not found({request})')
            raise SingleMessageError(JWT_NOT_EXIST) # 토큰이 없음

        # get_validated_token 을 통해 JWT 검증
        try:
            validated_token = self.get_validated_token(rawToken)
        except Exception as e:
            logger.error(f'CustomJWTAuthentication Exception({e})')
            raise SingleMessageError(JWT_INVALID)

        userID = validated_token['uid']
        try:
            user = User.objects.get(uid=userID)
        except User.DoesNotExist:
            logger.error(f'CustomJWTAuthentication User.DoesNotExist')
            raise SingleMessageError(USER_NOT_EXIST)
        
        logger.info(f'CustomJWTAuthentication success(uid:{userID})')
        
        return (user, None)