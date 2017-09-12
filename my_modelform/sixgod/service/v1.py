"""
1. 数据列表页面,定制显示烈
    示例一：
        v1.site.register(Model)， 默认只显示对象列表


    示例二：
        class SubClass(BaseYinGunAdmin):
            list_display = []

        v1.site.register(Model,SubClass), 按照list_display中指定的字段进行显示
        PS: 字段可以
                - 字符串，必须是数据库列明
                - 函数，
                    #     def comb(self,obj=None,is_header=False):
                    #         if is_header:
                    #             return "牟烈"
                    #         else:
                    #             return "%s-%s" %(obj.username,obj.email,)


            完整示例如下：
                # class YinGunUserInfo(v1.BaseYinGunAdmin):
                #
                #
                #     def func(self,obj=None,is_header=False):
                #         if is_header:
                #             return '操作'
                #         else:
                #             name = "{0}:{1}_{2}_change".format(self.site.namespace,self.model_class._meta.app_label,self.model_class._meta.model_name)
                #             url = reverse(name,args=(obj.pk,))
                #             return mark_safe("<a href='{0}'>编辑</a>".format(url))
                #
                #     def checkbox(self,obj=None,is_header=False):
                #         if is_header:
                #             # return mark_safe("<input type='checkbox'/>")
                #             return "选项"
                #         else:
                #             tag = "<input type='checkbox' value='{0}' />".format(obj.pk)
                #             return mark_safe(tag)
                #
                #     def comb(self,obj=None,is_header=False):
                #         if is_header:
                #             return "牟烈"
                #         else:
                #             return "%s-%s" %(obj.username,obj.email,)
                #
                #     list_display = [checkbox,'id','username','email',comb, func]
                #
                # v1.site.register(models.UserInfo,YinGunUserInfo)

"""

from django.shortcuts import render, HttpResponse, redirect
from django.shortcuts import reverse
from sixgod.utils.pager import PageInfo
import copy


class BaseSixGodAdmin(object):
    list_display = "__all__"

    add_or_edit_model_form = None

    action_list = []

    filter_list = []

    def __init__(self, model_class, site):
        self.model_class = model_class
        self.site = site
        self.request = None

        self.app_label = model_class._meta.app_label
        self.model_name = model_class._meta.model_name

    def get_add_or_edit_model_form(self):
        """
        封装ModelForm
        :return: 
        """
        if self.add_or_edit_model_form:
            return self.add_or_edit_model_form
        else:
            # 对象继承类，类继承type
            from django.forms import ModelForm
            class MyModelForm(ModelForm):
                class Meta:
                    model = self.model_class
                    fields = "__all__"
                    error_messages = {'username': {'required': '不可为空'}, 'email': {'required': '不可为空'},
                                      'ug': {'required': '不可为空'}, 'm2m': {'required': '不可为空'}, }

                # 添加class
                def __init__(self, *args, **kwargs):
                    super(MyModelForm, self).__init__(*args, **kwargs)

                    # for example change class for integerPolje1
                    # self.fields['integerPolje1'].widget.attrs['class'] = 'SOMECLASS'

                    # you can iterate all fields here
                    for fname, f in self.fields.items():
                        f.widget.attrs['class'] = 'form-control'
                        # 添加class 结束

            # _m = type('Meta', (object,), {'model': self.model_class, 'fields': "__all__"})
            # MyModelForm = type('MyModelForm', (ModelForm,), {'Meta': _m})
            return MyModelForm

    @property
    def urls(self):
        from django.conf.urls import url, include
        info = self.model_class._meta.app_label, self.model_class._meta.model_name  # 元组：app名，类名
        urlpatterns = [
            url(r'^$', self.changelist_view, name='%s_%s_changelist' % info),
            url(r'^add/$', self.add_view, name='%s_%s_add' % info),
            url(r'^(.+)/delete/$', self.delete_view, name='%s_%s_delete' % info),
            url(r'^(.+)/change/$', self.change_view, name='%s_%s_change' % info),

        ]
        return urlpatterns

    def changelist_view(self, request):
        # result_list = self.model_class.objects.all()

        # 生成添加按钮
        from django.http.request import QueryDict
        param_dict = QueryDict(mutable=True)
        if request.GET:
            param_dict['_changelistfilter'] = request.GET.urlencode()
            # 拼接参数
        base_add_url = reverse('{0}:{1}_{2}_add'.format(self.site.namespace, self.app_label,
                                                        self.model_name))
        add_url = '{0}?{1}'.format(base_add_url, param_dict.urlencode())
        self.request = request  # request传入self
        # 生成添加按钮 结束

        # 分页
        condition = {}
        base_list_url = reverse('{0}:{1}_{2}_changelist'.format(self.site.namespace, self.app_label,
                                                                self.model_name))
        # utl_path = request.path_info
        total_row = self.model_class.objects.filter(**condition).count()

        page_param_dict = copy.deepcopy(request.GET)  # 保持url其他参数，深拷贝request.GET，防止以后使用对其有影响
        page_param_dict._mutable = True  # querydict默认不可修改，_mutable=True可以修改

        page_info = PageInfo(request.GET.get('page'), total_row, base_list_url, page_param_dict)
        result_list = self.model_class.objects.filter(**condition)[page_info.start:page_info.end]
        # 分页 结束

        # action操作
        action_list = []
        for item in self.action_list:
            tpl = {'name': item.__name__, 'text': item.text}
            action_list.append(tpl)

        if request.method == "POST":
            action_name_str = request.POST.get('action')
            ret = getattr(self, action_name_str)(request)

            action_list_url = reverse('{0}:{1}_{2}_changelist'.format(self.site.namespace, self.app_label,
                                                                      self.model_name))
            if ret:
                action_list_url = '{0}?{1}'.format(action_list_url, request.GET.urlencode())

            return redirect(action_list_url)
        # action操作 结束

        # 组合查询
        from sixgod.utils.filter_code import FilterList
        filter_list = []
        for option in self.filter_list:
            if option.is_func:
                data_list = option.field_or_func(self, option, request)
            else:
                from django.db.models import ForeignKey, ManyToManyField, OneToOneField
                field = self.model_class._meta.get_field(option.field_or_func)
                if isinstance(field, ForeignKey):
                    data_list = FilterList(option, field.rel.model.objects.all(), request)
                elif isinstance(field, ManyToManyField):
                    data_list = FilterList(option, field.rel.model.objects.all(), request)
                else:
                    data_list = FilterList(option, field.model.objects.all(), request)
            filter_list.append(data_list)
        # 组合查询 结束

        context = {
            'result_list': result_list,  # QuerySet对象
            'list_display': self.list_display,  # 要显示的字段
            'basesixgodadmin_obj': self,
            'add_url': add_url,
            'page_info': page_info,
            'action_list': action_list,
            'filter_list': filter_list
        }
        return render(request, 'sg/change_list.html', context)

    def add_view(self, request):
        if request.method == "GET":
            form = self.get_add_or_edit_model_form()()
        else:
            form = self.get_add_or_edit_model_form()(data=request.POST, files=request.FILES)
            if form.is_valid():
                obj = form.save()

                popid = request.GET.get('popup')
                if popid:
                    context_dict = {'data_dict': {
                        'pk': obj.pk,
                        'text': str(obj),
                        'popid': popid
                    }}
                    return render(request, 'sg/popup_response.html', context_dict)
                else:
                    base_list_url = reverse(
                        '{2}:{0}_{1}_changelist'.format(self.app_label, self.model_name, self.site.namespace))
                    list_url = '{0}?{1}'.format(base_list_url, request.GET.get('_changelistfilter'))
                    return redirect(list_url)

        context = {'form': form}
        return render(request, 'sg/add.html', context)

    def delete_view(self, request, pk):
        obj = self.model_class.objects.filter(pk=pk).first()
        if not obj:
            return HttpResponse('ID不存在')
        if request.method == "GET":
            obj.delete()

        base_list_url = reverse(
            '{2}:{0}_{1}_changelist'.format(self.app_label, self.model_name, self.site.namespace))
        list_url = '{0}?{1}'.format(base_list_url, request.GET.get('_changelistfilter'))
        return redirect(list_url)

    def change_view(self, request, pk):
        obj = self.model_class.objects.filter(pk=pk).first()
        if not obj:
            return HttpResponse('ID不存在')
        if request.method == "GET":
            form = self.get_add_or_edit_model_form()(instance=obj)
        else:
            form = self.get_add_or_edit_model_form()(instance=obj, data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()

                base_list_url = reverse(
                    '{2}:{0}_{1}_changelist'.format(self.app_label, self.model_name, self.site.namespace))
                list_url = '{0}?{1}'.format(base_list_url, request.GET.get('_changelistfilter'))
                return redirect(list_url)

        context = {'form': form}
        return render(request, 'sg/edit.html', context)


class SixGodSite(object):
    def __init__(self):
        self._registry = {}
        self.namespace = 'sixgod'  # 用于反向生成url
        self.app_name = 'sixgod'

    def register(self, model_class, bsga=BaseSixGodAdmin):
        """
        将model类封装并加入_registry列表
        :param model_class: 
        :param bsga: 
        :return: 
        """
        self._registry[model_class] = bsga(model_class, self)  # 生成BaseSixGodAdmin对象封装了model类和SixGodSite类
        '''
        {
        UesrInfo类：BaseSixGodAdmin（UesrInfo类，SixGodSite对象） -> UesrInfo类：UserInfoBSGA（UesrInfo类，SixGodSite对象）
        Role：BaseSixGodAdmin（Role，SixGodSite对象）
        }
        '''

    def get_urls(self):
        """
        循环_registry列表中的model类，生成url
        :return: 
        """
        from django.conf.urls import url, include
        ret = []
        for model_cls, sixgod_admin_obj in self._registry.items():
            app_label = model_cls._meta.app_label
            model_name = model_cls._meta.model_name
            ret.append(url(r'^%s/%s/' % (app_label, model_name), include(sixgod_admin_obj.urls)))  # include路由分发

        return ret

    @property
    def urls(self):
        """
        调用get_urls方法
        :return: 
        """
        return self.get_urls(), self.app_name, self.namespace

    def login(self, request):
        return HttpResponse('login')


site = SixGodSite()
