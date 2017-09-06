from django.db import models


class UserInfo(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    email = models.EmailField(null=True)
    age = models.IntegerField(default=1)
    ug = models.ForeignKey('UserGroup')
    m2m = models.ManyToManyField('Role')

    def __str__(self):
        return self.username


class UserGroup(models.Model):
    title = models.CharField(max_length=32)

    def __str__(self):
        return self.title


class Role(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name
