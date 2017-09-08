from django.shortcuts import render, HttpResponse, reverse


def test(request):
    url = reverse('sixgod:app01_userinfo_changelist')
    url1 = reverse('sixgod:app01_userinfo_add')
    url2 = reverse('sixgod:app01_userinfo_change', args=(1,))
    url3 = reverse('sixgod:app01_userinfo_delete', args=(1,))
    print(url, '\n', url1, '\n', url2, '\n', url3)
    return HttpResponse('...')
