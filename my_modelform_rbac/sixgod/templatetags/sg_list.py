from django.template import Library
from types import FunctionType

register = Library()


def table_body(result_list, list_display, basesixgodadmin_obj):
    # v = []
    # for row in result_list:
    #     sub = []
    #     for name in list_display:
    #         if isinstance(name, FunctionType):
    #             sub.append(name.__name__.title)
    #         else:
    #             sub.append(getattr(row, name))
    #     v.append(sub)
    # return v

    for row in result_list:
        if list_display == "__all__":
            yield [str(row, ), ]
        else:
            yield [name(basesixgodadmin_obj, obj=row) if isinstance(name, FunctionType) else getattr(row, name) for name
                   in list_display]


def table_head(list_display, basesixgodadmin_obj):
    # v = []
    # for item in list_display:
    #     if isinstance(item, FunctionType):
    #         v.append(item.__name__.title())
    #     else:
    #         v.append(item)
    # return v

    # return [item.__name__.title() if isinstance(item, FunctionType) else item for item in list_display]

    if list_display == "__all__":
        yield '对象'
    else:
        for item in list_display:
            if isinstance(item, FunctionType):
                yield item(basesixgodadmin_obj, is_header=True)
            else:
                yield basesixgodadmin_obj.model_class._meta.get_field(item).verbose_name


@register.inclusion_tag('sg/md.html')
def operate(result_list, list_display, basesixgodadmin_obj):
    """
    return结果先经过md.html渲染再返回
    :param result_list: 
    :param list_display: 
    :return: 
    """
    b = table_body(result_list, list_display, basesixgodadmin_obj)
    h = table_head(list_display, basesixgodadmin_obj)
    return {'body': b, 'head': h}
