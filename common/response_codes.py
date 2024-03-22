"""
1000번대 - 단순 정보(서버의 상태) 전달
"""

"""
2000번대 - 성공
"""
REQUEST_SUCCESS = { "code" : 2000, "message" : "요청 성공", }

# 2100번대 - 회원 정보(로그인, 회원가입)
SIGNUP_SUCCESS = { "code" : 2100, "message" : "회원가입 성공", }
SIGNIN_SUCCESS = { "code" : 2110, "message" : "로그인 성공", }

"""
3000번대 - 리다이렉션
"""

"""
4000번대 - 요청 오류(클라이언트 요청 에러)
"""
# 4000 Bad Request
BAD_REQUEST = { "code" : 4000, "message" : "Bad Request", }
INVALID_INPUT = { "code" : 4001, "message" : "잘못된 입력입니다.", }

# 4100번대 - 회원 정보(로그인, 회원가입)
DUPLICATE_EMAIL = { "code" : 4100, "message" : "이메일 중복",  }
DUPLICATE_ID = { "code" : 4101, "message" : "아이디 중복",  }
DUPLICATE_NICKNAME = { "code" : 4102, "message" : "닉네임 중복",  }

REQUIRED_EMAIL = { "code" : 4103, "message" : "이메일을 입력해주세요.",  }
REQUIRED_ID = { "code" : 4104, "message" : "ID를 입력해주세요.",  }
REQUIRED_NICKNAME = { "code" : 4105, "message" : "닉네임을 입력해주세요.",  }
REQUIRED_PASSWORD = { "code" : 4106, "message" : "비밀번호를 입력해주세요.",  }

LENGTH_NICNNAME = { "code" : 4107, "message" : "닉네임은 2자 이상 20자 이하여야 합니다.",  }

USER_NOT_EXIST = { "code" : 4110, "message" : "유저 존재하지 않음", }
INCORRECT_PASSWORD = { "code" : 4111, "message" : "비밀번호 불일치", }
INVALID_EMAIL = { "code" : 4120, "message" : "유효하지 않은 이메일 형식", }


# 4400번대 - 소셜 로그인 오류
NONE_EXIST_SOCIAL_SEED = { "code" : 4400, "message" : "소셜 로그인 정보가 존재하지 않음", }
INVALID_SOCIAL_SEED = { "code" : 4401, "message" : "잘못된 로그인 인증 키 전송", }
REQUIRED_SOCIAL_SEED = { "code" : 4402, "message" : "존재하지 않는 로그인 인증 키 전송", }
EXPIRED_SOCIAL_SEED = { "code" : 4403, "message" : "인증 기간이 만료", }
DUPLICATE_SOCIAL_SEED = { "code" : 4404, "message" : "동일한 인증키 존재, 재전송 바람", }


# 4900번대 - 기타(인증 등)
JWT_NOT_EXIST = { "code" : 4900, "message" : "인증 토큰이 존재하지 않음", }
JWT_ATTRIBUTE_NOT_EXIST = { "code" : 4901, "message" : "인증 토큰 항목이 존재하지 않음", }
JWT_INVALID = { "code" : 4902, "message" : "유효하지 않은 토큰", }


"""
5000번대 - 서버 오류
"""
# 5000 - common error

# 5100 - USER 관련
SIGNUP_CLICK_CREATION_FAILED = { "code" : 5101, "message" : "유저 클릭 정보 생성 실패",  }

# 5200 - DATABASE ERROR
DATABASE_ERROR = { "code" : 5200, "message" : "데이터베이스 오류",  }
