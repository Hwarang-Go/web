from django.db import models

# Create your models here.


class Fruits(models.Model):
    name = models.CharField(max_length=50) # 객체를 만들고 있음(앞문자 대문자 - class) , 문자열 최대 50자 저장
    descript = models.TextField()  # 많은 문자 저장
    price = models.FloatField()  # 실수
    quantity = models.IntegerField()  # 정수
    cdate = models.DateTimeField(auto_now_add=True)  # DateTime 형식 / auto_now_add 는 데이터 들어갈때 그 시각을 적어라라는 DB기능

    def __str__(self):
        return 'id : {},name : {}, description : {}'.format(self.id, self.name, self.descript)