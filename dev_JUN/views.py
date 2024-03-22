from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from .models import Click, User

from rest_framework import serializers
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from common.response_codes import *
from common.response_functions import makeJsonResponse, makeJsonErrorResponse
from rest_framework.exceptions import ValidationError, ParseError
from common.common_exceptions import SingleMessageError

from django.core.cache import cache

# jwt 생성 관련
from rest_framework_simplejwt.tokens import AccessToken

# django Transaction
from django.db import transaction


"""
@date 2024-02-08
@author 정준이
@description 테스트 API
"""
def index(request):
    c = Click.objects.get(uid=1)
    print(c)
    c.click_cnt += 1
    c.save()
    return HttpResponse("Hello, World!")

"""
@date 2024-02-16
@updated 2024-02-16
@author 정준이
@description 테스트용 유저 조회 API
"""
def getUser(request, user_id):
    try:
        user = User.objects.get(uid=user_id)
        user_data = {
            'id': user.id,
            'nickname': user.nickname,
            'email': user.email,
        }
        return JsonResponse(user_data)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

"""
@date 2024-02-08
@updated 2024-02-16
@author 정준이
@description 회원가입 API
    request : SignUpRequestSerializer
    response : str
"""
@transaction.atomic()
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
        except ParseError as e:
            return makeJsonErrorResponse(BAD_REQUEST)

        userSerializer = SignUpRequestSerializer(data=data)

        try:
            # User 생성
            userSerializer.is_valid(raise_exception=True)
            createdUser = userSerializer.save()

            # Click 생성
            clickData = {
                'click_cnt': 0,
                'user_id': createdUser.uid,
            }
            clickSerializer = ClickSerializer(data=clickData)
            clickSerializer.is_valid(raise_exception=True)
            clickSerializer.save()

            return makeJsonResponse(REQUEST_SUCCESS, "회원가입 성공")
        except ValidationError as e:
            transaction.set_rollback(True)
            result = INVALID_INPUT
            attributes = e.detail
            if 'id' in attributes:
                code = attributes['id'][0].code
                if code == 'required':
                    result = REQUIRED_ID
                elif code == 'duplicate':
                    result = DUPLICATE_ID
            elif 'email' in attributes:
                code = attributes['email'][0].code
                if code == 'required':
                    result = REQUIRED_EMAIL
                elif code == 'invalid':
                    result = INVALID_EMAIL
                elif code == 'duplicate':
                    result = DUPLICATE_EMAIL
            elif 'nickname' in attributes:
                code = attributes['nickname'][0].code
                if code == 'required':
                    result = REQUIRED_NICKNAME
                elif code == 'duplicate':
                    result = DUPLICATE_NICKNAME
                elif code in ['min_length', 'max_length']:
                    result = LENGTH_NICNNAME
            elif 'password' in attributes:
                code = attributes['password'][0].code
                if code == 'required':
                    result = REQUIRED_PASSWORD
            return makeJsonErrorResponse(result)
        except Exception as e:
            transaction.set_rollback(True)
            return makeJsonErrorResponse(BAD_REQUEST)
    else:
        return makeJsonErrorResponse(BAD_REQUEST)

"""
@date 2024-02-08
@updated 2024-02-14
@author 정준이
@description ID/PW 로그인 API
    request : LoginRequestSerializer
    response : LoginResponseSerializer
"""
def signin(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = LoginRequestSerializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
            id = serializer.validated_data['id']
            password = serializer.validated_data['password']
            obj = User.objects.filter(id=id).first()
            if obj is None:
                return makeJsonErrorResponse(USER_NOT_EXIST)

            if password == obj.password:
                user = User.objects.get(id=id)
                token = CustomTokenObtainPairSerializer.get_token(user)
                result = {
                    "token" : str(token.access_token),
                    "tk" : str(token),
                }
                response = LoginResponseSerializer(data=result)
                response.is_valid()
                
                return makeJsonResponse(REQUEST_SUCCESS, response.data)
            else:
                return makeJsonErrorResponse(INCORRECT_PASSWORD)
        except ValidationError as e:
            result = INVALID_INPUT
            attributes = e.detail
            if 'id' in attributes:
                code = attributes['id'][0].code
                if code == 'required':
                    result = REQUIRED_ID
            elif 'password' in attributes:
                code = attributes['password'][0].code
                if code == 'required':
                    result = REQUIRED_PASSWORD
            return makeJsonErrorResponse(result)
    else:
        return makeJsonErrorResponse(BAD_REQUEST)

            


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

#@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def jwtTest(request):
    print("Here")
    if request.method == 'GET' or request.method == 'POST':
        # Token에서 인증된 user만 가져온다.
        user = request.user
        print(f"user 정보 : {user}")
        if not user:
            return JsonResponse({"error": "접근 권한이 없습니다."}, status=401)
        return JsonResponse({"message": "Accepted"})