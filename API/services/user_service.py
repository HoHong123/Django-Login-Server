from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from API.models import Click, User, ClickTimeChallenge, OauthLogin
from API.serializers import *

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ValidationError, ParseError

from common.response_codes import *
from common.response_functions import makeJsonResponse, makeJsonErrorResponse
from common.common_exceptions import SingleMessageError

from django.core.cache import cache

# jwt 생성 관련
from rest_framework_simplejwt.tokens import AccessToken

# django Transaction
from django.db import transaction

from HWS.settings.base import BASE_LOGGER

import logging

logger = logging.getLogger(BASE_LOGGER)

"""
@date 2024-02-21
@updated 2024-02-21
@author 정준이
@description 회원가입 서비스
@param 
    1. serializers.SignUpRequestSerializer signUpRequestSerializer
"""
@transaction.atomic()
def createUser(signUpRequestSerializer):
    try:
        # User 생성
        signUpRequestSerializer.is_valid(raise_exception=True)
        createdUser = signUpRequestSerializer.save()
        
        # Click 생성
        clickData = {
            'click_cnt': 0,
            'user_id': createdUser.uid,
        }
        clickSerializer = ClickSerializer(data=clickData)
        clickSerializer.is_valid(raise_exception=True)
        createdClick = clickSerializer.save()

        # ClickTimeChallenge 생성
        clickTimeChallengeData = {
            'click_cnt': 0,
            'user_id': createdUser.uid,
        }
        caselickTimeChallengeSerializer = ClickTimeChallengeSerializer(data=clickTimeChallengeData)
        caselickTimeChallengeSerializer.is_valid(raise_exception=True)
        createdClickTimeChallenge = caselickTimeChallengeSerializer.save()

        result = {
            'uid':createdUser.uid,
        }

        return makeJsonResponse(REQUEST_SUCCESS, result)
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
        logger.error(f'Fail to create User data (Result:{result})(Detail:{e})')
        return makeJsonErrorResponse(result)
    except Exception as e:
        logger.error(f'Fail to create User data ({e})')
        transaction.set_rollback(True)
        return makeJsonErrorResponse(BAD_REQUEST)

"""
@date 2024-02-22
@updated 2024-02-22
@author 정준이
@description jwt 발급 서비스
@param 
    1. models.User
"""
def issueJWT(user):
    try:
        token = CustomTokenObtainPairSerializer.get_token(user)
        
        result = {
            "token" : str(token.access_token),
        }
        
        response = SigninResponseSerializer(data=result)
        response.is_valid()
        
        logger.info(f'issueJWT Response({user.uid})')
        
        return makeJsonResponse(REQUEST_SUCCESS, response.data)
    except User.DoesNotExist:
        logger.error(f'issueJWT User.DoesNotExist')
        return makeJsonErrorResponse(USER_NOT_EXIST)
    except ValidationError as e:
        result = INVALID_INPUT
        attributes = e.detail
        logger.error(f'issueJWT ValidationError({e})')
        return makeJsonErrorResponse(result)
    except Exception as e:
        logger.error(f'issueJWT Exception({e})')
        return makeJsonErrorResponse(BAD_REQUEST)


"""
@date 2024-02-22
@updated 2024-02-22
@author 정준이
@description 일반 로그인 서비스
@param 
    1. serializers.SigninRequestSerializer
"""
def commonSignIn(signinRequestSerializer):
    try:
        signinRequestSerializer.is_valid(raise_exception=True)
        id = signinRequestSerializer.validated_data['id']
        password = signinRequestSerializer.validated_data['password']
        obj = User.objects.filter(id=id).first()
        if obj is None:
            response = makeJsonErrorResponse(USER_NOT_EXIST)
            logger.warning(f'commonSignIn obj is None({id})')
            return response
        if password == obj.password:
            user = User.objects.get(id=id)
            logger.info(f'commonSignIn password is equal({id})')
            return issueJWT(user)
        else:
            logger.warning(f'commonSignIn password is not equal({id})')
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
        logger.error(f'commonSignIn ValidationError(Result:{result})(Detail:{e})')
        return makeJsonErrorResponse(result)


"""
@date 2024-02-21
@updated 2024-02-21
@author 정준이
@description 닉네임 수정 서비스
@param 
    1. serializers.PatchNicknameRequestSerializer
"""
def modifyUserNickname(patchNicknameRequestSerializer):
    try:
        patchNicknameRequestSerializer.is_valid(raise_exception=True)
        uid = patchNicknameRequestSerializer.data['uid']
        nickname = patchNicknameRequestSerializer.data['nickname']
        user = User.objects.get(uid=uid)
        user.nickname = nickname
        user.save()

        result = {
            'uid' : uid,
            'nickname' : nickname,
        }
        
        response = makeJsonResponse(REQUEST_SUCCESS, result)
        logger.info(f'modifyUserNickname Response({response})')
        
        return response
    except User.DoesNotExist:
        logger.error(f'modifyUserNickname User.DoesNotExist(uid:{uid})')
        return makeJsonErrorResponse(USER_NOT_EXIST)
    except ValidationError as e:
        result = INVALID_INPUT
        attributes = e.detail
        if 'nickname' in attributes:
            code = attributes['nickname'][0].code
            if code == 'required':
                result = REQUIRED_NICKNAME
            elif code == 'duplicate':
                result = DUPLICATE_NICKNAME
            elif code in ['min_length', 'max_length']:
                result = LENGTH_NICNNAME
        logger.error(f'modifyUserNickname ValidationError(Result:{result})(Detail:{e})')
        return makeJsonErrorResponse(result)
    except Exception as e:
        logger.error(f'modifyUserNickname Exception({e})')
        return makeJsonErrorResponse(BAD_REQUEST)
    

"""
@date 2024-02-21
@updated 2024-02-21
@author 정준이
@description 일반 클릭 점수 추가 서비스
@param 
    1. serializers.PostClickRequestSerializer
"""
def earnClickPoint(postClickRequestSerializer):
    try:
        postClickRequestSerializer.is_valid(raise_exception=True)
        uid = postClickRequestSerializer.data['uid']
        click_count = postClickRequestSerializer.data['click']
        click = Click.objects.get(user_id=uid)
        click.click_cnt += click_count
        click.save()

        result = {
            'uid' : uid,
            'click' : click.click_cnt,
        }
        
        response = makeJsonResponse(REQUEST_SUCCESS, result)
        logger.info(f'earnClickPoint Response({response})')
        
        return response
    except Click.MultipleObjectsReturned or Click.DoesNotExist:
        logger.error(f'earnClickPoint Click.MultipleObjectsReturned or Click.DoesNotExist(uid:{uid})')
        return makeJsonErrorResponse(DATABASE_ERROR)
    except ValidationError as e:
        result = INVALID_INPUT
        attributes = e.detail
        logger.error(f'earnClickPoint ValidationError({e})')
        return makeJsonErrorResponse(result)
    except Exception as e:
        logger.error(f'earnClickPoint Exception({e})')
        return makeJsonErrorResponse(BAD_REQUEST)
    
"""
@date 2024-02-21
@updated 2024-02-21
@author 정준이
@description 타임어택 기록 갱신 서비스
@param 
    1. serializers.PostRecordTimeChallengeRequestSerializer
"""
def recordTimeChallenge(postRecordTimeChallengeRequestSerializer):
    try:
        postRecordTimeChallengeRequestSerializer.is_valid(raise_exception=True)
        uid = postRecordTimeChallengeRequestSerializer.data['uid']
        clickRecord = postRecordTimeChallengeRequestSerializer.data['click']
        latestRecord = ClickTimeChallenge.objects.get(user_id=uid)

        if latestRecord.click_cnt < clickRecord :
            latestRecord.click_cnt = max(latestRecord.click_cnt, clickRecord)
            latestRecord.save()

        result = {
            'uid' : uid,
            'click' : latestRecord.click_cnt,
        }
        
        response = makeJsonResponse(REQUEST_SUCCESS, result)
        logger.info(f'recordTimeChallenge Response({response})')
        
        return response
    except ClickTimeChallenge.MultipleObjectsReturned or ClickTimeChallenge.DoesNotExist:
        logger.error(f'recordTimeChallenge ClickTimeChallenge.MultipleObjectsReturned or ClickTimeChallenge.DoesNotExist(uid:{uid})')
        return makeJsonErrorResponse(DATABASE_ERROR)
    except ValidationError as e:
        result = INVALID_INPUT
        attributes = e.detail
        logger.error(f'recordTimeChallenge ValidationError({e})')
        return makeJsonErrorResponse(result)
    except Exception as e:
        logger.error(f'recordTimeChallenge Exception({e})')
        return makeJsonErrorResponse(BAD_REQUEST)


"""
@date 2024-02-23
@updated 2024-02-23
@author 박기홍
@description 소설 로그인 테이블 확인
@param 
    1. str 난수값
"""
def createSocialLoginRecord(socialLoginSerializer):
    try:
        socialLoginSerializer.is_valid(raise_exception=True)
        socialLoginSerializer.save()
        
        response = makeJsonResponse(REQUEST_SUCCESS, 'Create Social Login Record')
        logger.info(f'Social Login data save Response({response})')
        
        return response
    except Exception as e:
        logger.error(f'Social seed Exception({e})')
        return makeJsonErrorResponse(BAD_REQUEST)

"""
@date 2024-02-22
@updated 2024-02-22
@author 정준이
@description 일반 클릭 랭킹 조회 서비스
@param
    number : a number describes how many user to retrieve in the ranking
"""
def selectClickRanking(number):
    topClickRanking = Click.objects.order_by('-click_cnt', 'uid')[:number].values('user_id', 'click_cnt')
    ranked_data = []
    for idx, entry in enumerate(topClickRanking, start=1):
        entry['rank'] = idx
        ranked_data.append(entry)
    
    response = makeJsonResponse(REQUEST_SUCCESS, list(topClickRanking))
    logger.info(f'selectClickRanking Response({response})')
    
    return response


"""
@date 2024-02-23
@updated 2024-02-23
@author 정준이
@description 타임어택 랭킹 조회 서비스
@param
    number : a number describes how many user to retrieve in the ranking
"""
def selectTimeChallengeRanking(number):
    topClickRanking = ClickTimeChallenge.objects.order_by('-click_cnt', 'uid')[:number].values('user_id', 'click_cnt')
    ranked_data = []
    for idx, entry in enumerate(topClickRanking, start=1):
        entry['rank'] = idx
        ranked_data.append(entry)
        
    response = makeJsonResponse(REQUEST_SUCCESS, list(topClickRanking))
    logger.info(f'selectTimeChallengeRanking Response({response})')
    
    return response