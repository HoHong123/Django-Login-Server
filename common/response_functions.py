from django.http import JsonResponse

"""
@date 2024-02-08
@author 정준이
@description JSON 응답 포맷에 따라 응답하는 함수
@parameter
    responseCode : response_code.py 에 정의된 응답 코드
    result : 응답할 JSON 에 첨부할 결과
"""
def makeJsonResponse(responseCode, result) :
    response = {
        "result" : result,
        "code" : responseCode["code"],
        "message" : responseCode["message"],
    }

    return JsonResponse(response)

"""
@date 2024-02-08
@author 정준이
@description JSON 에러 포맷에 따라 응답하는 함수
@parameter
    responseCode : response_code.py 에 정의된 응답 코드
"""
def makeJsonErrorResponse(responseCode) :
    response = {
        "code" : responseCode["code"],
        "message" : responseCode["message"],
    }

    return JsonResponse(response)