from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Board, Topic, Post
from .forms import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
    board = get_object_or_404(Board, pk=pk)
    # 基于函数的视图实现分页
    """
    board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    由于上面的代码执行结果超出预期，这种FBV基于函数的视图实现分页的方式暂时不可取
    本代码引起的错误还有是Replies模块，本人已向作者提交问题，同时也希望各位大佬能够解决
    """
    queryset = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 20)
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics.paginator.page(1)
    except EmptyPage:
        topics.paginator.page(paginator.num_pages)
    return render(request, 'new_topics.html', {'board': board, 'topics': topics})
    # topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    # return render(request, 'new_topics.html', {'board': board, 'topics': topics})


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
    topic.views += 1
    topic.save()
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


"""
GCBV基于类的通过视图实现编辑
"""


class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)


class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'new_topics.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        self.topic.views += 1
        self.topic.save()
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset
