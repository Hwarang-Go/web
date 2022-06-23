from django.shortcuts import render
from product.models import Fruits


def createFruitsGet(request):
    return render(request, "product/create.html")


def createFruitsPost(request):
    fruit = Fruits()
    fruit.name = request.POST.get('fname', None)
    fruit.descript = request.POST.get('fdescript', None)
    fruit.price = request.POST.get('fprice', None)
    fruit.quantity = request.POST.get('fquantity', None)

    fruit.save()  # 상속받아온 model.Model에 있는 save 사용해서 database에 저장
    # ORM, 알아서 SQL 문으로 바꿔서 저장해준다는것~

    return render(request, "product/createResult.html")


def readFruitGet(request):
    fruits = Fruits.objects.all()
    # objects : django가 모델에 알아서 objects 라는 객체를 심어둠
    # db에서 한행한행을 하나의 객체로 해서 objects.all()하면 모든 객체들을 받아옴
    # ORM으로 모든 데이터를 조회하는 것이라고 생각하면 됨. SQL 문으로 변환되서 요청될것임
    print(fruits)
    fruit_id1 = Fruits.objects.filter(id=1)
    print(fruit_id1)
    context = {
        'fruits': fruits,
        'fruit_id1': fruit_id1
    }
    return render(request, "product/list.html", context)