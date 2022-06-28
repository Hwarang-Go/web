from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

from board.forms import PostForm
from board.models import Post, PostImage
from reply.forms import ReplyForm
from reply.models import Reply


def mainPage(request):
    # posts = Post.objects.all().order_by('-id')
    posts = Post.objects.prefetch_related('reply_set').all()
    return render(request, 'board/index.html', {'posts': posts})


# def createGet(request):
#     postForm = PostForm() # form 객체를 받아옴
#     context = {
#         'postForm': postForm
#     } # 전달해줄 context는 항상 dictionary 타입인 것 기억
#     return render(request, "board/create.html", context)

# django 에서 지원하는 데코레이터 (자바의 어노테이션)
# 달기만 하면 기능이 추가됨
# login_url 속성을 넣어서 로그인 안되어있으면 해당 url로 이동
@login_required(login_url='/accounts/login')
def create(request):
    if request.method == 'GET':
        # postForm = PostForm() # form 객체를 받아옴
        # context = {
        #     'postForm': postForm
        # } # 전달해줄 context는 항상 dictionary 타입인 것 기억
        return render(request, "board/create.html") #, context)
    elif request.method == 'POST':
        postForm = PostForm(request.POST)
        if postForm.is_valid():  # 값들의 유효성 검사
            post = postForm.save(commit=False)
            post.writer = request.user # 사용자 정보 추가
            post.save()

            # save images
            # request.FILES.getlist 로 업로드된 파일들 불러옴
            for image in request.FILES.getlist('image', None):
                print(image)
                postImage = PostImage()
                print(postImage)
                postImage.image = image
                postImage.post = post
                postImage.save()
        return redirect('/board/read/'+str(post.id))
        # 게시글 생성 후에 리스트가 아니라 그 게시글이 보이도록 리다이렉트
        #return render(request, "board/createResult.html")
    # method 하나로 createGet, createPost 모두 처리
    # -> GET, POST 방식을 메소드 하나로 처리

def list(request):
    # posts = Post.objects.all()
    # 정렬 은 order_by(): 기본은 오름차순,
    # 내림차순은 id 기준으로 '-' 붙여서 하면 됨
    posts = Post.objects.prefetch_related('postimage_set').order_by('-id')

    # testPost = Post.objects.filter(title='test') # filer test
    # requset.GET.get('id', id_num) 으로 특정 아이디 불러와서 할수도있음

    context = {
        'posts':posts,
        # 'testPost':testPost
    }
    return render(request, "board/list.html", context)

def read(request, bid):
    # path를 통해 넘어온 bid 변수는 인자로 받을수 있음(request.GET.get() 이거 안쓰고)
    # posts = Post.objects.filter(id=bid) # filter, all 로 받아오면 query set을 리스트로 반환 받음 (1개만 불러와도)
    # post = Post.objects.get(Q(id=bid)) # 하나만 받아옴, Q 는 쿼리, 하나만 할땐 안써도 됨
    post = Post.objects\
        .prefetch_related('reply_set')\
        .prefetch_related('postimage_set')\
        .get(id=bid) # 기본 형태: 썩 좋지 않음. 나중에 고도화 함(SQL 필요)
    # 이제 post 에는 id, title, contents, writer, "reply_set" 이 있음
    # prefetch_related 인자로는 관계를 맺고 있는 가지고 오고 싶은 모델을 _set 붙여서 씀 _set
    # context = {'post': post} # render 인자로 context 넘길 때 context 는 dictionary 타입임 그냥 dictionary 로 바로 넘겨줌
    # 안에 들어갈 내용이 많다면 위 방밥이 더 좋을듯
    replyForm = ReplyForm()

    return render(request, 'board/read.html', {'post': post, 'replyForm': replyForm})
    # return render(request, 'board/read.html', {'post': post, 'replyForm': replyForm, 'replys': replys})
    # replys = Reply.objects.all()
    # 나는 처음에 그냥 다 가져와서 html에서 템플릿 문법으로 구분해줬었음
    # reply 가져오기
    # 1) select_related
    #   - Reply 에 Post 관계가 있는 경우 같을 때 사용
    #   - 정방향
    #   - join SQL 방법으로 가져와
    # 2) prefetch_related
    #   - Post에 Reply 가 없는 경우 같을 때 사용
    #   - 역방향
    #   - 쿼리를 2개가 실행됨 : 프레임워크에 따라 성능이 다름, django 는 Query Set cash 에 저장해두고 result cash... ORM에서 자세히 다룸


@login_required(login_url='/accounts/login')
def delete(request, bid):
    post = Post.objects.get(id=bid)
    if request.user != post.writer:
        return redirect('/board/list')
    post.delete()
    return redirect('/board/list')
    # render 말고 redirect 지워지는 화면으로 다시 안돌아가게

@login_required(login_url='/accounts/login')
def update(request, bid):
    post = Post.objects.get(id=bid)
    if request.method == 'GET':
        # update form 을 보여주는 페이지로 bid와 함께 이동 url은 update/bid
        postForm = PostForm(instance=post)
        # 폼 생성한 후, 기존 내용 채워주기 위해서 instance=post[조회한 게시글] 설정
        context = {
            'postForm': postForm
        }
        if request.user != post.writer:
            return redirect('/board/read/' + str(post.id))
        return render(request, 'board/update.html', context)
        # 어차피 update랑 create 양식 똑같아서 일단 실습대로 create 사용
        # return render(request, 'board/update.html', context)
    elif request.method == 'POST':
        postForm = PostForm(request.POST, instance=post)
        # postForm = PostForm(request.POST)
        # 처음 아래처럼, 그리고 위에처럼 하면 아래 수정 부분 바꿀수 있음
        if postForm.is_valid():  # 값들의 유효성 검사
            # 수정 후에 저장
            # post.title = postForm.cleaned_data['title']
            # post.contents = postForm.cleaned_data['contents']
            post = postForm.save(commit=False)
            post.save()
        return redirect('/board/read/'+str(post.id))


@login_required(login_url='/accounts/login')
def like(request, bid):
    # 누르면 게시글에 좋아요 추가
    post = Post.objects.get(id=bid)
    user = request.user
    if post.like.filter(id=user.id).exists():
        # 왜 그냥 id?
        # django 에서 내가 넣은게 user.id면 알아서 user_id로 해줌
        post.like.remove(user)
        return JsonResponse({'message': 'deleted', 'like_cnt': post.like.count()})
    # 백엔드에서 like_cnt를 세서 전달해주고 있음 -> 비효율적으로 짜보신다는데 왜 비효율적이지?
    # 이미 프론트에 like를 다 받아둔 상태인데 쓸데없는 통신을 더 하게 되기 때문
    #  (프론트에서 100개 였다면 하트 취소 시 -1 해서 99개로 그냥 보여주면 됨)
    else:
        post.like.add(user)  # manytomany 해놔서 되는거
    # board_post_like 테이블에 보면 post_id, user_id 필요해서 위 코드처럼 post 가져오고 request.user 를 같이 주는 것
    return JsonResponse({'message': 'added', 'like_cnt': post.like.count()})

