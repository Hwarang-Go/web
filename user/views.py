from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
# Create your views here.

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


