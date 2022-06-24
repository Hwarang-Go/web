from user.models import User
from django.db import models


class Post(models.Model):  # django 가 만들어둔 models.Model 을 상속받아온다
    title = models.CharField(max_length=100)
    contents = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    # ForeignKey 외래키 : '누구'(다른 모델)를 참조하겠다.
    # User 는 django에서 지원해주는 모델(우리는 만든적이 없다)
    # 데이터 베이스 규칙
        # writer 에 쓸수 있는 값은 User 모델에 있는 값(회원 가입되어있는 회원)
        # or Null 값 만 가능
    # on_delete :
    #   user01로 글쓰고 user01이 탈퇴를 해버리면?
    #   user01이 지워질 때 어떻게 할거냐고 묻는 속성
    #       1) 게시글도 같이 지운다
    #           - models.CASCADE
    #       2) Null 값으로 한다.
    # 위에 데이터베이스 규칙에 따라 없어진 사용자 때문에 오류가 날 수 있기 때문

    # writer 추가 후에 makemigrations 했을 때 경고 안내가 나옴
    # 원래 없던 writer row에 대해 어떻게 처리를 할 것인가
    # 1) 기본값을 넣겠다(null)
    # 2) 수동으로 따로 지정을 하겠다.
    # 예제에서는 1번 선택 > 기본값을 입력 (기본키)

    # makemigrations 끝내고 나니 board app에 migrations 폴더에 새로운 파일 생성됨
    # 새파일: 여기까지 설정이 된거야~

    like = models.ManyToManyField(User, related_name="likes", blank=True)
    # 다 : 다 관계
    # blank 는 입력이 되지 않아도 되도록 하는 속성
    # writer에  User 관계와 겹쳐서 참조할 때 구분이 안가서
    # related_name="likes" 를 해서 참조할 떄 저 이름을 쓰도록 함
