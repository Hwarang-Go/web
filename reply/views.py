import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from board.models import Post
from reply.forms import ReplyForm
from reply.models import Reply


@login_required(login_url='/accounts/login')
@csrf_exempt
def createReply(request, bid):
    # if request.method == 'GET':
    #     replyForm = ReplyForm()  # form 객체를 받아옴
    #     return render(request, "reply/create.html", {'replyForm': replyForm})
    # board/read/bid 의 화면에서 입력을 받기 떄문에 위의 코드 비활성화
    if request.method == 'POST':
        replyForm = ReplyForm(request.POST)
        if replyForm.is_valid():  # 값들의 유효성 검사
            print('aaa')
            reply = replyForm.save(commit=False)
            reply.writer = request.user
            post = Post()
            post.id = bid
            reply.post = post # Post 모델의 객체가 reply.post 에 들어가야하므로 위 2줄과 같은 과정 필요
            # reply.post = Post.objects.get(id=bid) # 이렇게 하면 안되나? 근데 오버헤드가 위에게 더 작긴 할듯
            reply.save()
        return redirect('/board/read/' + str(bid))
        # reply = Reply()
        # data = json.loads(request.body)
        # data = json.dumps(data)
        # print(data, '****************************************************************')
        # reply.contents = data.contents
        # post = Post()
        # post.id = bid
        # reply.post = post
        # reply.writer = request.user
        # reply.save()
        # return HttpResponse('ok')


        # return redirect('/board/read/' + str(bid))
        # return redirect('reply/read/' + str(reply.id))
        # return HttpResponse("reply 저장")


def readReplyList(request):
    replys = Reply.objects.all().order_by('-id')

    print(replys)
    # requset.GET.get('id', id_num) 으로 특정 아이디 불러와서 할수도있음

    return render(request, 'reply/list.html', {'replys': replys,})


def readReplyOne(request, rid):
    # try except 문은 없는 id로 접근할 때 예외처리 하기위해서 임의로 작성한 코드
    try:
        reply = Reply.objects.get(Q(id=rid))  # 하나만 받아옴, Q 는 쿼리, 하나만 할땐 안써도 됨
    except Reply.DoesNotExist:
        reply = None
    if reply is None:
        return redirect('/reply/list')
    else:
        return render(request, 'reply/read.html', {'reply':reply})


@login_required(login_url='/accounts/login')
def updateReply(request, rid):
    reply = Reply.objects.get(id=rid)
    if request.method == 'GET':
        replyForm = ReplyForm(instance=reply)
        if request.user != reply.writer:
            return redirect(request, '/board/read/' + str(reply.post_id))
        return render(request, 'reply/create.html', {'replyForm':replyForm})
    elif request.method == 'POST':
        replyForm = ReplyForm(request.POST, instance=reply)
        if replyForm.is_valid():  # 값들의 유효성 검사
            reply = replyForm.save(commit=False)
            reply.save()
        return redirect('/board/read/' + str(reply.post_id))


@login_required(login_url='/accounts/login')
def deleteReply(request, rid):
    reply = Reply.objects.get(id=rid)
    if request.user != reply.writer:
        return redirect('/board/read/' + str(reply.post_id))
    reply.delete()
    return redirect('/board/read/' + str(reply.post_id))


@login_required(login_url='/accounts/login')
def replyLike(request, rid):
    # 누르면 게시글에 좋아요 추가
    reply = Reply.objects.get(id=rid)
    user = request.user
    if reply.reply_like.filter(id=user.id).exists():
        reply.reply_like.remove(user)
        return JsonResponse({'message': 'deleted', 'like_cnt': reply.reply_like.count()})
    else:
        reply.reply_like.add(user)
    return JsonResponse({'message': 'added', 'like_cnt': reply.reply_like.count()})