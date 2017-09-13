from django.template import Library
from types import FunctionType
from django.forms.models import ModelChoiceField
from sixgod.service import v1
from django.urls import reverse

register = Library()


@register.inclusion_tag('sg/add_edit_form.html')
def show_add_edit_form(form):
    """
    return结果先经过md.html渲染再返回
    :param result_list: 
    :param list_display: 
    :return: 
    """
    form_list = []
    for item in form:
        row = {'is_popup': False, 'item': None, 'popup_url': None}
        if isinstance(item.field, ModelChoiceField) and item.field.queryset.model in v1.site._registry:
            target_app_label = item.field.queryset.model._meta.app_label
            target_model_name = item.field.queryset.model._meta.model_name
            url_name = '{0}:{1}_{2}_add'.format(v1.site.namespace, target_app_label, target_model_name)
            target_url = '{0}?popup={1}'.format(reverse(url_name), item.auto_id)

            row['is_popup'] = True
            row['item'] = item
            row['popup_url'] = target_url
        else:
            row['item'] = item
        form_list.append(row)

    return {'form': form_list}
