import logging
from django.db import models
from supermap.models.user import User
logger = logging.getLogger(__name__)


class UserInviteRecord(models.Model):
    inviter_id = models.BigIntegerField(verbose_name='邀请人')
    invitee_id = models.BigIntegerField(verbose_name='被邀请人')
    day = models.IntegerField(verbose_name='日期(年月日)')
    rewards = models.FloatField(default=0, verbose_name='奖励数值')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    @property
    def inviter_name(self):
        try:
            return User.objects.get(id=self.inviter_id).nickname
        except User.DoesNotExist:
            return None

    @property
    def invitee_name(self):
        try:
            return User.objects.get(id=self.invitee_id).nickname
        except User.DoesNotExist:
            return None

    class Meta:
        db_table = "user_invite_record"
