class FilterList(object):
    def __init__(self, option, data_list):
        self.option = option
        self.data_list = data_list

    def show(self):
        self.option.nick()

    def __iter__(self):
        yield '全部：'
        for i in self.data_list:
            yield "<a href='{0}'>{1}</a>".format(i, self.option.bs + i)


class FilterOption(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def nick(self):
        tpl = self.name + str(self.age)
        return tpl

    @property
    def bs(self):
        if self.age > 15:
            return "大"
        else:
            return "小"


obj_list = [
    FilterList(FilterOption('吕布', 19), ['貂蝉', '汗血宝马']),
    FilterList(FilterOption('孙权', 14), ['小乔', '陆逊', '江东']),
    FilterList(FilterOption('司马懿', 22), ['司马昭', '司马孚', ]),
    FilterList(FilterOption('曹操', 12), ['鸡肋', '白脸', '关羽'])
]

for obj in obj_list:
    for item in obj:
        print(item, end='')
    else:
        print('')
