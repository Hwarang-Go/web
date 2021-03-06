from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import board.views
import reply.views
import user.views

urlpatterns = [
    path('admin/', admin.site.urls),  # 앞에 'admin/'이 id값이고, admin.site.urls 가 실제 접근할 경로
    path('', board.views.mainPage),
    # path('product/create', product.views.createFruitsGet),
    # path('product/createPost', product.views.createFruitsPost),
    # path('product/list', product.views.readFruitGet),

    # board
    path('board/create', board.views.create),
    path('board/list', board.views.list),
    path('board/read/<int:bid>', board.views.read), # <int:bid> : 변수
    path('board/delete/<int:bid>', board.views.delete),
    path('board/update/<int:bid>', board.views.update),

    # like (in board)
    path('like/<int:bid>', board.views.like),
    path('reply-like/<int:rid>', reply.views.replyLike),


    # Reply
    path('reply/create/<int:bid>', reply.views.createReply),
    path('reply/list', reply.views.readReplyList),
    path('reply/delete/<int:rid>', reply.views.deleteReply),
    path('reply/read/<int:rid>', reply.views.readReplyOne),
    path('reply/update/<int:rid>', reply.views.updateReply),
    path('replyUpdate', reply.views.update),

    # User
    # path('user/signup', user.views.signup),
    path('user/login', user.views.login),
    # path('user/logout', user.views.logout),
    path('user/changeProfilePhoto', user.views.changeProfilePhoto),

    # allauth
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', user.views.profile),

    # Kakao login
    path('kakaoLogin', user.views.kakaoLoginPage),
    path('oauth/redirect', user.views.getcode),

    # test path
    # path('account/login_test', user.views.login_test),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
22.06.16 (목)
url 관련해서 trailing slash 검색해서 더 알아볼것
abc 와 abc/ 는 다른 url 임

    만약 처음에 abc/ 로 작업한 후에 크롬에서 abc 실행하면 django에서 자동으로 / 붙여서 redirect 시켜주고 크롬 캐시에 저장됨, 
    그 후에 코드에서 abc 로 변경하여 다시 접근하려고 하면,
    django에서 url은 abc인데 크롬 캐시로 인해 abc/ 로 접근하려고 하여 error가 발생함.

관련한 검색 키워드로 django trailing slash, url slug, 등을 참고해 볼 것.
"""
