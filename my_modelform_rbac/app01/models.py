from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=32, verbose_name='角色名称')

    def __str__(self):
        return self.name


class UserGroup(models.Model):
    title = models.CharField(max_length=32, verbose_name='组名')

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    username = models.CharField(max_length=32, verbose_name='用户名')
    email = models.CharField(max_length=32, verbose_name='邮箱')
    ug = models.ForeignKey(UserGroup, verbose_name='科室')
    m2m = models.ManyToManyField(Role, verbose_name='角色')

    def text_username(self):
        return self.username

    def value_username(self):
        return self.username

    def text_email(self):
        return self.email

    def value_email(self):
        return self.email
