from django.db import models
from django.contrib.auth.models import User


# Create your models here.


# 模板类
class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)
    # 不写此方法 会出现一下情况：
    """
    <QuerySet [<Board: Board object (1)>, <Board: Board object (2)>]>
    """

    def __str__(self):
        return self.name


# 主题类
class Topic(models.Model):
    subject = models.CharField(max_length=25)
    last_update = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.CASCADE)
    starter = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now_add=True)


# 帖子类
class Post(models.Model):
    message = models.CharField(max_length=4000)
    # 即在外键值的后面加上 on_delete=models.CASCADE
    """
    原因：
        在django2.0后，定义外键和一对一关系的时候需要加on_delete选项，此参数为了避免两个表里的数据不一致问题，不然会报错：
        TypeError: __init__() missing 1 required positional argument: 'on_delete'
    """
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)
