from tortoise import fields
from tortoise.models import Model


class TenantUser(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=100, unique=True)
    email = fields.CharField(max_length=100, null=True)
    hashed_password = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)
    is_owner = fields.BooleanField(default=False)
