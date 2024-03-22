from django.http.response import HttpResponseRedirect
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.conf import settings

from rest_framework.exceptions import ValidationError

from API.services.user_service import *
from API.serializers import *

from dev_PKH.google_backend import GoogleAuthBackend

import logging

logger = logging.getLogger(BASE_LOGGER)


def loginView(request):
    return render(request, 'home.html')

def loginFailView(request):
    return render(request, 'login_fail.html')

def loginSuccessView(request):
    return render(request, 'login_success.html')

def logoutView(request):
    logout(request)
    return redirect("/login/")

def googleLogin(request):
    seed = request.GET.get('seed')
    
    if seed is None:
        return redirect("/login/fail/")
    
    googleRedirect = settings.GOOGLE_LOGIN_REDIRECT_URI + "&state=" + seed
    
    # Redirect to google login page
    return HttpResponseRedirect(googleRedirect)

def googleLoginParam(request, param):
    if param is None:
        return redirect("/login/fail/")
    
    googleRedirect = settings.GOOGLE_LOGIN_REDIRECT_URI
    googleRedirect += "&state=" + param
    
    # Redirect to google login page
    return HttpResponseRedirect(googleRedirect)

def googleLoginTablecheck(request, param):
    if request.method == 'GET':
        if param is None:
            return makeJsonErrorResponse(REQUIRED_SOCIAL_SEED)
        
        try:
            login = OauthLogin.objects.get(hash=param)
            uid = login.user_id
            
            if login.IsRecordExpired():
                response = makeJsonErrorResponse(EXPIRED_SOCIAL_SEED)
            else:
                response = issueJWT(User.objects.get(uid=uid))
            
            login.delete()
            return response
        except (OauthLogin.DoesNotExist, User.DoesNotExist) as e:
            logger.error(f'DoesNotExist Error 로그인 오류 ({e})')
            return makeJsonErrorResponse(NONE_EXIST_SOCIAL_SEED)
        except (OauthLogin.MultipleObjectsReturned, User.MultipleObjectsReturned) as e:
            logger.error(f'MultipleObjectsReturned Error 로그인 오류 ({e})')
            return makeJsonErrorResponse(DATABASE_ERROR)
        except Exception as e:
            logger.error(f'ERROR::Social login check fail with parameter \"{param}\" ({e})')
    return makeJsonErrorResponse(BAD_REQUEST)

def googleCallback(request):
    logger.info(f'Request recived ({request})')
    print(request)
    
    # if callbkac is error
    if 'error' in request.GET:
        logger.error(f'Request 오류 ({request})')
        return redirect('login/')

    # if callback is succesfully done
    code = request.GET.get('code')
    if code is None:
        logger.warning(f'REQUEST ERROR::code not found')
        return redirect('/login/fail/')
    
    try:
        googleAccess = GoogleAuthBackend()
        googleAccount = googleAccess.authenticate(request, code)
        logger.info(f'Google API callback succeed with ({googleAccount})')
        
        if googleAccount:
            user = socialLogin(googleAccount)
            logger.info(f'Create Google User data. name({user.email}), id({user.id}), nickname({user.nickname})')
            
            # Save hash data to Login Table
            hash = { 
                    'hash':request.GET.get('state'),
                    'user_id':user.uid
                }
            
            loginSerializer = SocialCheckRequestSerializer(data=hash)
            createSocialLoginRecord(loginSerializer) # 난수 로그인 테이블 값 생성
            
            return redirect('/login/success/')
    except ValidationError as e:
        logger.error(f'Validation Error 로그인 오류 ({e})')
        return redirect('/login/fail/')
    except Exception as e:
        logger.error(f'Unknown Error 로그인 오류 ({e})')
        return redirect('/login/fail/')

def socialLogin(request):
    email = request.get('email')
    queryset = User.objects.filter(email=email)
    
    if queryset.exists() is False: # 회원 정보 없으면 회원가입 실행
        logger.info(f'Google account \"{email}\" is new to our service, Proceed to signup')
        
        id = email + '_GoogleID'
        password = 'HitUP_' + id
        userDict = {
            'id':id,
            'email':email,
            'password':password,
            'social_idp':1
        }
        
        userSerializer = SignUpRequestSerializer(data=userDict)
        createUser(userSerializer)

    try:
        user = queryset.get(email=email)
    except Exception as e:
        logger.error(f'Google account \"{email}\" signup fail with an error message ({e})')
        return redirect('/login/fail')
    
    return user
