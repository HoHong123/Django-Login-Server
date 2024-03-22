from django.shortcuts import render

from django.http import HttpResponse
from django.forms.models import model_to_dict

from django.http import HttpResponse, JsonResponse
from .models import Click, User

from .serializers import *
from rest_framework.parsers import JSONParser
from common.response_codes import *
from common.response_functions import makeJsonResponse, makeJsonErrorResponse
from rest_framework.exceptions import ValidationError, ParseError

from django.core.cache import cache
from API.services import user_service

# django Transaction
from django.db import transaction

# JWT Authentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from HWS.settings.base import BASE_LOGGER
import logging

logger = logging.getLogger(BASE_LOGGER)

"""
@date 2024-02-20
@author 정준이
@description 테스트 API
"""
def index(request):
    return HttpResponse("Hello, World!")

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
        userData = {
            'id': user.id,
            'nickname': user.nickname,
            'email': user.email,
        }
        return JsonResponse(userData)
    except User.DoesNotExist:
        logger.error(f'getUser User not found User.DoesNotExist({user_id})')
        return JsonResponse({'error': 'User not found'}, status=404)
    
"""
@date 2024-02-23
@updated 2024-02-23
@author 정준이
@description 자신 정보 조회 API
"""
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def selectMyself(request):
    # Token에서 인증된 user만 가져온다.
    user = request.user
    if not user:
        return makeJsonErrorResponse(JWT_INVALID)
    uid = user.uid

    return user_service.getUserByUid(uid)

"""
@date 2024-02-08
@updated 2024-02-21
@author 정준이
@description 회원가입 API
    request : SignUpRequestSerializer
    response : str
"""
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
        except ParseError as e:
            logger.error(f'signup ParseError({e})')
            return makeJsonErrorResponse(BAD_REQUEST)
        
        data['social_idp'] = 0
        signUpRequestSerializer = SignUpRequestSerializer(data=data)
        
        logger.info(f'signup success ({data["id"]}, {data["email"]})')
        
        return user_service.createUser(signUpRequestSerializer)
    else:
        logger.error(f'signup request.method is not POST({request})')
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
        try:
            data = JSONParser().parse(request)
        except ParseError as e:
            logger.error(f'signin ParseError({e})')
            return makeJsonErrorResponse(BAD_REQUEST)
        signinRequestSerializer = SigninRequestSerializer(data=data)
        
        logger.info(f'signin success ({data["id"]})')
        
        return user_service.commonSignIn(signinRequestSerializer)
    else:
        logger.error(f'signin request.method is not POST({request})')
        return makeJsonErrorResponse(BAD_REQUEST)


"""
@date 2024-02-21
@updated 2024-02-21
@author 정준이
@description 닉네임 수정 API
    request : PatchNicknameRequestSerializer
"""
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateNickname(request):
    # Token에서 인증된 user만 가져온다.
    user = request.user
    if not user:
        logger.error(f'updateNickname user is None')
        return makeJsonErrorResponse(JWT_INVALID)
    
    try:
        data = JSONParser().parse(request)
    except ParseError as e:
        logger.error(f'updateNickname ParseError({e})')
        return makeJsonErrorResponse(BAD_REQUEST)
    
    data['uid'] = user.uid

    patchNicknameRequestSerializer = PatchNicknameRequestSerializer(data=data)
    
    logger.info(f'updateNickname success ({data["uid"]}, {data["nickname"]})')
    
    return user_service.modifyUserNickname(patchNicknameRequestSerializer)


"""
@date 2024-02-21
@updated 2024-02-21
@author 정준이
@description 일반 클릭 점수 추가 API
    request : PatchNicknameRequestSerializer
"""
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def clickUp(request):
    # Token에서 인증된 user만 가져온다.
    user = request.user
    if not user:
        logger.error(f'clickUp user is None')
        return makeJsonErrorResponse(JWT_INVALID)
    try:
        data = JSONParser().parse(request)
    except ParseError as e:
        logger.error(f'clickUp ParseError({e})')
        return makeJsonErrorResponse(BAD_REQUEST)
    
    data['uid'] = user.uid
    
    postClickRequestSerializer = PostClickRequestSerializer(data=data)
    
    logger.info(f'clickUp success ({data["uid"]})')
    
    return user_service.earnClickPoint(postClickRequestSerializer)



"""
@date 2024-02-22
@updated 2024-02-22
@author 정준이
@description 타임어택(Time Challenge) 기록 갱신 API
"""
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def clickTimeChallengeRecord(request):
    # Token에서 인증된 user만 가져온다.
    user = request.user
    if not user:
        logger.error(f'clickUp user is None')
        return makeJsonErrorResponse(JWT_INVALID)
    try:
        data = JSONParser().parse(request)
    except ParseError as e:
        logger.error(f'clickTimeChallengeRecord ParseError({e})')
        return makeJsonErrorResponse(BAD_REQUEST)
    
    data['uid'] = user.uid
    
    postRecordTimeChallengeRequestSerializer = PostRecordTimeChallengeRequestSerializer(data=data)
    
    logger.info(f'clickTimeChallengeRecord success ({data["uid"]})')
    
    return user_service.recordTimeChallenge(postRecordTimeChallengeRequestSerializer)

"""
@date 2024-02-22
@updated 2024-02-22
@author 정준이
@description 일반 클릭 랭킹 조회 API
"""
def showClickRanking(request, number):
    if request.method == 'POST':
        number = max(0, number)
        number = min(100, number)
        return user_service.selectClickRanking(number)
    else:
        return makeJsonErrorResponse(BAD_REQUEST)
    

"""
@date 2024-02-23
@updated 2024-02-23
@author 정준이
@description 타임어택 랭킹 조회 API
"""
def showTimeChallengeRanking(request, number):
    if request.method == 'POST':
        number = max(0, number)
        number = min(100, number)
        return user_service.selectTimeChallengeRanking(number)
    else:
        return makeJsonErrorResponse(BAD_REQUEST)