from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Board, Topic, Post
from django.contrib.auth.models import User
from .forms import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    boards = Board.objects.all()
    boards_name = list()
    boards_description = list()
    for board in boards:
        boards_name.append(board.name)
        boards_description.append(board.description)
    response_name = '<br>'.join(boards_name)
    response_space = '<br>'
    response_description = '<br>'.join(boards_description)
    return HttpResponse(response_name + response_space + response_description)


def test(request):
    boards = Board.objects.all()
    return render(request, 'new_home.html', {'boards': boards})


def board_topics(request, pk):
    board = Board.objects.get(pk=pk)
    return render(request, 'new_topics.html', {'board': board})


'''使用HTML自带form操作方法'''

# def new_topic(request, pk):
#     board = get_object_or_404(Board, pk=pk)
#
#     if request.method == "POST":
#         subject = request.POST["subject"]
#         message = request.POST["message"]
#
#         user = User.objects.first()  # 临时使用一个账号作为登录用户
#
#         topic = Topic.objects.create(
#             subject=subject,
#             board=board,
#             starter=user
#         )
#
#         post = Post.objects.create(
#             message=message,
#             topic=topic,
#             created_by=user
#         )
#         return redirect('board_topics', pk=board.pk)
#     return render(request, 'new_topic.html', {'board': board})

'''使用Django自带的Form API方法操作'''


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == "POST":  # 判断表单提交方式
        form = NewTopicForm(request.POST)
        if form.is_valid():  # 判断是否可以存到数据库
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()  # save() ⽅法返回⼀个存⼊数据库的 Model 实例
            post = Post.objects.create(
                message=form.cleaned_data.get("message"),
                topic=topic,
                created_by=request.user
            )
            return redirect("topic_posts", pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()
    return render(request, "new_topic.html", {"board": board, "form": form})


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    return render(request, 'topic_posts.html', {'topic': topic})


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        form = PostForm()
        return render(request, 'reply_topic.html', {'topic': topic, 'form': form})
