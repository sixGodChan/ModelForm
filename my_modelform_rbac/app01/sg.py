from sixgod.service import v1
from app01 import models
from django.utils.safestring import mark_safe
from django.shortcuts import reverse


class UserInfoBSGA(v1.BaseSixGodAdmin):  # UserInfoBSGA类 继承BaseSixGodAdmin 并封装 list_display 和
    def change(self, obj=None, is_header=False):
        if is_header:
            return '操作'
        else:
            # name = "{0}:{1}_{2}_change".format(self.site.namespace, self.model_class._meta.app_label,
            #                                    self.model_class._meta.model_name)
            # url = reverse(name, args=(obj.pk,))
            # 生成编辑连接
            from django.http.request import QueryDict
            param_dict = QueryDict(mutable=True)
            if self.request.GET:
                param_dict['_changelistfilter'] = self.request.GET.urlencode()
            # 凭借url和参数
            base_edit_url = reverse("{0}:{1}_{2}_change".format(self.site.namespace, self.model_class._meta.app_label,
                                                                self.model_class._meta.model_name), args=(obj.pk,))
            edit_url = '{0}?{1}'.format(base_edit_url, param_dict.urlencode())
            tag = '<a href="{0}">编辑</a>'.format(edit_url)
            return mark_safe(tag)

    def checkbox(self, obj=None, is_header=False):
        if is_header:
            return mark_safe('<input type="checkbox"/>')
        else:
            tag = '<input name="pk" type="checkbox" value="{0}"/>'.format(obj.pk)
            return mark_safe(tag)

    def delete(self, obj=None, is_header=False):
        if is_header:
            return '操作'
        else:
            # 生成编辑连接
            from django.http.request import QueryDict
            param_dict = QueryDict(mutable=True)
            if self.request.GET:
                param_dict['_changelistfilter'] = self.request.GET.urlencode()
            # 凭借url和参数
            base_delete_url = reverse("{0}:{1}_{2}_delete".format(self.site.namespace, self.model_class._meta.app_label,
                                                                  self.model_class._meta.model_name), args=(obj.pk,))
            delete_url = '{0}?{1}'.format(base_delete_url, param_dict.urlencode())
            tag = '<a href="{0}">删除</a>'.format(delete_url)
            return mark_safe(tag)

    list_display = [checkbox, 'id', 'username', 'email', change, delete]

    def initial(self, request):
        pk_list = request.POST.getlist('pk')
        models.UserInfo.objects.filter(pk__in=pk_list).update(username='雎鸠')
        return True

    initial.text = '初始化'

    def multi_del(self, request):
        pk_list = request.POST.getlist('pk')
        models.UserInfo.objects.filter(pk__in=pk_list).delete()
        return True

    multi_del.text = '批量删除'

    action_list = [initial, multi_del]

    from sixgod.utils.filter_code import FilterOption

    def email(self, option, request):
        from sixgod.utils.filter_code import FilterList
        queryset = models.UserInfo.objects.filter(id__gt=2)
        return FilterList(option, queryset, request)

    filter_list = [
        FilterOption('username', False, text_func_name='text_username', val_func_name='value_username'),
        FilterOption(email, False, text_func_name='text_email', val_func_name='value_email'),
        FilterOption('ug', True),
        FilterOption('m2m', False)
    ]


v1.site.register(models.UserInfo, UserInfoBSGA)  # 调用v1.site.register方法


class RoleBSGA(v1.BaseSixGodAdmin):
    # list_display = [checkbox, 'id', 'name', change]
    list_display = ['id', 'name']


v1.site.register(models.Role)

v1.site.register(models.UserGroup)
