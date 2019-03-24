"""Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from learn import views as learn_views
from boards import views as boards_views
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # 新加的URL
    # path('', learn_views.home),
    # path('', boards_views.home),
    path('', boards_views.test, name='board_test'),

    # Django 1.+ url匹配规则
    # url((r'^boards/(?P<pk>\d+)/$', boards_views.board_topics, name='board_topics'),
    # url((r'^boards/(?P<pk>\d+)/new/$', boards_views.new_topic, name='new_topic'),

    # Django2.+ path 匹配规则
    #  path('boards/<int:pk>/', boards_views.board_topics, name='board_topics'),
    path('boards/<int:pk>/new/', boards_views.new_topic, name='new_topic'),

    # 注册
    path('signup/', accounts_views.signup, name='signup'),

    # 注销
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # 登录
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    # 密码重置
    path('reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
        email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt'
    ),
         name='password_reset'),
    path('reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html')),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    # Django2.+中的正则表达方式
    re_path('reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})',
            auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
            name='password_reset_confirm'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_rest_complete'),

    # 修改密码
    path('setting/password', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
         name='password_change'),

    # 修改密码完成
    path('setting/password/done', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
         name='password_change_done'),

    # 主题回复
    # path('boards/<int:pk>/topics/<int:topic_pk>', boards_views.topic_posts, name='topic_posts'),
    path('boards/<int:pk>/topics/<int:topic_pk>/reply/', boards_views.reply_topic, name='reply_topic'),

    # # FBV 基于函数的视图
    # path('new_post/', boards_views.new_post, name='new_post'),
    #
    # # CBV 基于类的视图
    # path('new_post/', boards_views.NewPostView.as_view(), name='new_post'),
    #
    # # GCBV 基于类的通过视图
    # path('new_post/', boards_views.NewPost.as_view, name='new_post'),

    # 通过GCBV的方式实现编辑
    path('boards/<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/edit/ ',
         boards_views.PostUpdateView.as_view(), name='edit_post'),

    # 基于GCBV实现分页
    path('boards/<int:pk>/', boards_views.TopicListView.as_view(), name='board_topics'),
    path('boards/<int:pk>/topics<int:topic_pk>', boards_views.PostListView.as_view(), name='topic_posts'),

    path('index/', learn_views.index),
    path('second/', learn_views.second),
    path('third/', learn_views.third),
    path('add/', learn_views.add, name='add'),
    path('add2/<int:a>/<int:b>', learn_views.add2, name='add2'),
]
