import os

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from user.models import User
from config.settings import BASE_DIR
import requests

def getcode(request):
    code = request.GET.get('code', None)  # 인가 코드
    # http 프로토콜로 카카오 api 에게 요청
    data = {
        'grant_type': 'authorization_code',
        'client_id': 'a24f138319b3c2e78b7befe47821f2cd',
        'redirect_uri': 'http://127.0.0.1:8000/oauth/redirect',
        'code': code,
    }
    headers = {
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
    }
    res = requests.post('https://kauth.kakao.com/oauth/token', data=data, headers=headers)
    token_json = res.json()
    print(token_json)
    access_token = token_json['access_token']
    # 액세스 토큰으로 사용자 정보 받아와서 우리 디비에 저장시키는게 목적

    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    res = requests.get('https://kapi.kakao.com/v2/user/me', headers=headers)
    # res = requests.post('https://kapi.kakao.com/v2/user/me', headers=headers)
    # 위의 요청은 get, post 모두 가능
    profile_json = res.json()


    kakaoid = profile_json['id']
    user = User.objects.filter(email=kakaoid)
    if user.exists():
        print('aaa')
        auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    else:
        print('bbb')
        # 불러온 회원이 없으면
        user = User()
        user.username = profile_json['properties']['nickname']
        user.email = kakaoid
        user.save()


    # 추가로 해볼 것은 db에 칼럼 하나 만들고 어떤 소셜로그인을 통해 가입했는지 기록


    return redirect('/board/list')

def kakaoLoginPage(request):
    secret_file = os.path.join(BASE_DIR, 'secret.json')
    with open(secret_file) as f:
        import json
        secrets = json.loads(f.read())  # json 타입의 변수에 secret.json 파일 내용 받아옴

    return render(request, 'login.html', secrets)


def signup(request):
    if request.method == 'GET':
        # 회원 가입 페이지
        # django에서 주는 form
        # django.conrib.auth 는 이미 프로젝트 만들때 APP에 추가되있음
        # DB도 마이그레이션 하고 보면 auth 관련 테이블들 나와있음
        signupForm = UserCreationForm()
        return render(request, 'user/signup.html', {'signupForm':signupForm})

    if request.method == 'POST':
        # DB 저장
        signupForm = UserCreationForm(request.POST)
        print(signupForm)
        if signupForm.is_valid(): # 패스워드 조건 안맞추면 여기서 다 걸림
            # input 값에 name이 "username", "password1", "password2" 가 필요했음
            user = signupForm.save(commit=False)
            user.save()
        return redirect('/user/login')


def logout(request):
    auth_logout(request) # 이것도 원래는 django의 logout 인데 겹쳐서 as 로 다른 이름 씀
    return redirect('/user/login')

def login(request):
    if request.method == 'GET':
        # 로그인 페이지
        loginForm = AuthenticationForm()
        return render(request, 'user/login.html', {'loginForm': loginForm})
    elif request.method == 'POST':
        # 실제 user 데이터 조회
        loginForm = AuthenticationForm(request, request.POST)
        # 로그인 할때 인자로 request, request.POST 둘다 들어가는 것을 주의
        if loginForm.is_valid():
            # 아래 auth_login은 원래 login 이라는 이름의 함수인데
            # login 이라는 함수가 나에게 있어서 as auth_login 으로 import 할때 바꿔서 씀
            auth_login(request, loginForm.get_user())
            # django에서 지원하는 login 함수는 세션 방식 (여기서는 auth_login)
            return redirect('/board/list')
            """
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = User.objects.POST.get(username=username)
            if user.password == password:
                # 로그인 성공
            else:
                # 로그인 실패

            이 과정을 위의 auth_login 으로 끝내버림
            """
            # return redirect('/board/list')

@login_required(login_url='/accounts/login')
def profile(request):
    return render(request, 'user/profile.html')

def changeProfilePhoto(request):
    user = request.user
    user.image = request.FILES.get('profile_image', None)
    user.save()
    return redirect('/accounts/profile')


# def login_test(request):
#     return render(request, 'account/login_test.html')