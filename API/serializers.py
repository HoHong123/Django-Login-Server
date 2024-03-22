from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import ValidationError

from .models import User, Click, ClickTimeChallenge, OauthLogin

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
@date 2024-02-22
@updated 2024-02-14
@author 정준이
@description 타임어택 기록 Serializer
"""
class ClickTimeChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClickTimeChallenge
        fields = ['uid', 'click_cnt', 'user_id', 'created_at', 'updated_at']


"""
@date 2024-02-21
@updated 2024-02-21
@author 정준이
@description 회원가입 Serializer
"""
class SignUpRequestSerializer(serializers.ModelSerializer):
    # 이메일 양식 검증
    id = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    social_idp = serializers.IntegerField(default=0)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'social_idp']

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
    uid = serializers.IntegerField(required=True)
    nickname = serializers.CharField(required=True, min_length=2, max_length=20)

    class Meta:
        model = User
        fields = ['uid', 'nickname']

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
class SigninRequestSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        fields = ['id', 'password']

"""
@date 2024-02-14
@updated 2024-02-21
@author 정준이
@description 로그인용 응답 Serializer
로그인 응답시 필요한 JSON 구조를 명시하기 위함
"""
class SigninResponseSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)

    class Meta:
        fields = ['token']


"""
@date 2024-02-08
@update 2024-02-22
@author 정준이
@description JWT 발급용 Serializer
기본 제공되는 JWT 토큰 발급 후 payload에 추가 정보 적재
"""
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # token['nickname'] = user.nickname
        # token['id'] = user.id
        # token['social_idp'] = user.social_idp
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data
    

"""
@date 2024-02-21
@updated 2024-02-21
@author 정준이
@description 일반 클릭 점수 추가 Serializer
"""
class PostClickRequestSerializer(serializers.Serializer):
    uid = serializers.IntegerField(required=True)
    click = serializers.IntegerField(required=True)

    class Meta:
        fields = ['click', 'uid']

"""
@date 2024-02-21
@updated 2024-02-21
@author 정준이
@description 타임어택 기록 갱신 Serializer
"""
class PostRecordTimeChallengeRequestSerializer(serializers.Serializer):
    uid = serializers.IntegerField(required=True)
    click = serializers.IntegerField(required=True)

    class Meta:
        fields = ['click', 'uid']


"""
@date 2024-02-23
@updated 2024-02-23
@author 박기홍
@description 구글 로그인 여부 확인
"""
class SocialCheckRequestSerializer(serializers.ModelSerializer):
    hash = serializers.CharField(required=True)
    user_id = serializers.IntegerField(required=True)
    
    class Meta:
        model = OauthLogin
        fields = ['hash', 'user_id']

    def validate_hash(self, value):
        if OauthLogin.objects.filter(hash=value).exists():
            raise serializers.ValidationError("This hash is already in use.", code="duplicate")
        return value
