from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=100, unique=True)
    email = fields.CharField(max_length=100, unique=True, null=True)
    hashed_password = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)


class Organization(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    owner = fields.ForeignKeyField("models.User", related_name="organizations")
    created_at = fields.DatetimeField(auto_now_add=True)
