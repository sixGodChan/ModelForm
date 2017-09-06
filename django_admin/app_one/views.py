from django.shortcuts import render, redirect, HttpResponse
from django.forms import Form
from django.forms import widgets as fwidgets
from django.forms import fields as ffields
from app_one import models

from django.forms import ModelForm


class testModelForm(ModelForm):
    class Meta:
        model = models.UserInfo
        fields = '__all__'
        # exclude = ('password',)
        labels = {
            'username': '用户名',
            'email': '邮箱',
            'password': '密码',
            'ug': '科室',
            'm2m': '角色',
        }
        help_texts = {
            'username': 'help_text',
            'email': 'help_text',
            'password': 'help_text',
            'ug': 'help_text',
            'm2m': 'help_text'
        }
        error_messages = {
            'username': {'required': '用户名不能为空'},
            'password': {'required': '密码不能为空'},
            'email': {'required': '邮箱不能为空', 'invalid': '邮箱格式错误'}
        }
        # widgets = {
        #     'username': fwidgets.Textarea(attrs={'class': 's1'})
        # }
        # field_classes = {'username': ffields.EmailField}
        # localized_fields = {}


def test(request):
    if request.method == "GET":
        form = testModelForm()
        context = {'form': form}
        return render(request, 'test.html', context)
    else:
        form = testModelForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('...')
        context = {'form': form}
        return render(request, 'test.html', context)


"""
class testForm(Form):
    username = fields.CharField(required=True)
    password = fields.CharField(required=True, widget=widgets.Input(attrs={'type': 'password'}))
    email = fields.EmailField(required=True)
    ug_id = fields.ChoiceField(widget=widgets.Select, choices=[])
    m2m_id = fields.MultipleChoiceField(widget=widgets.SelectMultiple,
                                        choices=models.Role.objects.values_list('id', 'name'))

    def __init__(self, *args, **kwargs):
        super(testForm, self).__init__(*args, **kwargs)
        self.fields['ug_id'].choices = models.UserGroup.objects.values_list('id', 'title')


def test(request):
    if request.method == "GET":
        form = testForm()
        context = {'form': form}
        return render(request, 'test.html', context)
    else:
        form = testForm(request.POST)
        if form.is_valid():
            m2m_id = form.cleaned_data.pop('m2m_id')
            user_obj = models.UserInfo.objects.create(**form.cleaned_data)
            user_obj.m2m.add(*m2m_id)
            return HttpResponse('...')
        context = {'form': form}
        return render(request, 'test.html', context)
"""


def edit(request, nid):
    obj = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = testModelForm(instance=obj)
        context = {'form': form}
        return render(request, 'test.html', context)
    else:
        form = testModelForm(data=request.POST, instance=obj, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('...')
        context = {'form': form}
        return render(request, 'edit.html', context)
