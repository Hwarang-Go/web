from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # 프로필 사진으로 유저와 프로필 사진을 1 : 1 관계로 만들고 싶으면 아래 코드 활성 시키면 됨!
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    pass