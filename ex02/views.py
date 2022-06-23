from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def func1(request):
    return render(request, "ex02/func1.html")


def formtag(request):
    return render(request, "ex02/formtag.html")

def getData(request):

    userid = request.POST.get('userid', None)
    userpw = request.POST.get('userpw', None)
    print(userid, userpw)
    return HttpResponse('전송되었습니다.')