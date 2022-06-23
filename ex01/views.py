from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def func1(request):
    # return HttpResponse('Django 수업 입니다.')  # 생성자에게 인자를 넘겨서 객체를 생성하고 있음
    if request.GET.get('num1', None) is not None:
        numVar1 = request.GET.get('num1', None) # None을 안적어도 되지만 없으면 나중에 오류가 날수도 있어서 적는게 좋다고 함
        numVar2 = request.GET.get('num2', None)
        result = int(numVar1) + int(numVar2)
        print(result)

        context = {'key1': result}
        return render(request, 'page1.html', context)
    else:
        return render(request, 'page1.html')


def func2(request):
    return render(request, 'input.html')


def getPost(request):
    num1 = request.POST.get('num1', None)
    num2 = request.POST.get('num2', None)
    return HttpResponse(int(num1) + int(num2))


def testTrailingSlash(request):
    return HttpResponse('trailing test')