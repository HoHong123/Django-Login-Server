from django.utils import timezone
from django.db import models


class CommonDateColumns:
    created_at = models.DateTimeField(db_column='CREATED_AT', blank=False, null=False, auto_now_add=True)
    updated_at = models.DateTimeField(db_column='UPDATED_AT', blank=False, null=False, auto_now=True)

class Click(models.Model, CommonDateColumns):
    uid = models.BigAutoField(db_column='UID', primary_key=True)
    click_cnt = models.BigIntegerField(db_column='CLICK_CNT', default=0)
    user_id = models.BigIntegerField(db_column='USER_ID', unique=True)

    class Meta:
        managed = False
        db_table = 'CLICK'

class ClickTimeChallenge(models.Model, CommonDateColumns):
    uid = models.BigAutoField(db_column='UID', primary_key=True)
    click_cnt = models.IntegerField(db_column='CLICK_CNT', default=0, db_comment='time challenge record')
    user_id = models.BigIntegerField(db_column='USER_ID', unique=True)

    class Meta:
        managed = False
        db_table = 'CLICK_TIME_CHALLENGE'

class OauthLogin(models.Model):
    uid = models.BigAutoField(db_column='UID', primary_key=True)
    hash = models.CharField(db_column='HASH', max_length=512, null=True)
    user_id = models.BigIntegerField(db_column='USER_ID', unique=False, db_comment='for user table')
    created_at = models.DateTimeField(db_column='CREATED_AT', blank=False, null=False, auto_now_add=True)
    updated_at = models.DateTimeField(db_column='UPDATED_AT', blank=False, null=False, auto_now=True)

    def IsRecordExpired(self, recordDuractionBySecond=300):
        now = timezone.now()
        then = self.created_at
        time_difference = now - then
        return time_difference.total_seconds() > recordDuractionBySecond
    
    class Meta:
        managed = False
        db_table = 'OAUTH_LOGIN'

class User(models.Model, CommonDateColumns):
    uid = models.BigAutoField(db_column='UID', primary_key=True)
    id = models.CharField(db_column='ID', unique=True, max_length=256)
    email = models.CharField(db_column='EMAIL', unique=True, max_length=256)
    password = models.CharField(db_column='PASSWORD', max_length=512)
    nickname = models.CharField(db_column='NICKNAME', null=True, unique=True, max_length=20)
    social_idp = models.SmallIntegerField(db_column='SOCIAL_IDP', default=0, db_comment='0=ordinary, 1=google, 2=naver, 3=kakao')

    def is_authenticated(self):
        return True

    class Meta:
        managed = False
        db_table = 'USER'