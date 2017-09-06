from django.contrib import admin
from app_one import models


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'email', 'ug',)
    list_filter = ('ug',)


class GroupAdmin(admin.ModelAdmin):
    list_display = ('title',)


class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(models.UserInfo, UserAdmin)
admin.site.register(models.UserGroup)
admin.site.register(models.Role)
