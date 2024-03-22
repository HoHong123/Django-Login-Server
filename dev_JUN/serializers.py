from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import ValidationError

from .models import User, Click

# from common.response_codes import responseCodes
from common.response_codes import *
from common.common_exceptions import SingleMessageError
#from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


"""
@date 2024-02-08
@updated 2024-02-14
@author 정준이
@description 유저 일반클릭 수 Serializer
"""
class ClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Click
        fields = ['uid', 'click_cnt', 'user_id', 'created_at', 'updated_at']


"""
@date 2024-02-08
@updated 2024-02-16
@author 정준이
@description 회원가입 Serializer
"""
class SignUpRequestSerializer(serializers.ModelSerializer):
    # 이메일 양식 검증
    id = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    social_idp = serializers.IntegerField(required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password']

    def validate_id(self, value):
        if User.objects.filter(id=value).exists():
            raise serializers.ValidationError("This ID is already in use.", code="duplicate")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This Email is already in use.", code="duplicate")
        return value
    
"""
@date 2024-02-16
@updated 2024-02-16
@author 정준이
@description 닉네임 수정 Serailizer
"""
class PatchNicknameRequestSerializer(serializers.ModelSerializer):
    # 이메일 양식 검증
    nickname = serializers.CharField(required=True, min_length=2, max_length=20)

    class Meta:
        model = User
        fields = ['nickname']

    def validate_nickname(self, value):
        if User.objects.filter(nickname=value).exists():
            raise serializers.ValidationError("This Nickname is already in use.", code="duplicate")
        return value


"""
@date 2024-02-08
@author 정준이
@description 로그인용 Serializer
로그인 요청시 필요한 JSON 파싱
"""
class LoginRequestSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        fields = ['id', 'password']

"""
@date 2024-02-14
@author 정준이
@description 로그인용 Serializer
로그인 응답시 필요한 JSON 구조를 명시하기 위함
"""
class LoginResponseSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    tk = serializers.CharField(required=True)

    class Meta:
        fields = ['token', 'tk']


"""
@date 2024-02-08
@author 정준이
@description JWT 발급용 Serializer
기본 제공되는 JWT 토큰 발급 후 payload에 추가 정보 적재
"""
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['nickname'] = user.nickname
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data