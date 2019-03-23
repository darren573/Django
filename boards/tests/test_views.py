from django.test import TestCase
from django.urls import reverse
from ..views import home, board_topics, new_topic
from django.urls import resolve
from ..models import Board


# Create your tests here.

# class HomeTests(TestCase):
#     def test_home_view_status_code(self):
#         url = reverse('home')
#         response = self.client.get(url)
#         self.assertEquals(response.status_code, 200)
#
#     def test_home_url_resolves_home_view(self):
#         view = resolve('/')
#         self.assertEquals(view.func, home)


# 测试新标题类
class NewTopicTests(TestCase):
    # 创建⼀个测试中使⽤的 Board 实例
    def setUp(self):
        Board.objects.create(name="Django", description="Django Board")

    # 检查发给 view 的请求是否成功
    def test_new_topic_view_success_status_code(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    # 检查当 Board 不存在时 view 是否会抛出⼀个 404 的错误
    def test_new_topic_view_not_found_status_code(self):
        url = reverse('new_topic', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    # 检查是否正在使⽤正确的 view
    def test_new_topic_url_resolves_new_topic_view(self):
        view = resolve('/boards/1/new/')
        self.assertEquals(view.func, new_topic)

    # 确保导航能回到 topics 的列表
    def test_new_topic_view_contains_link_to_board_topics_view(self):
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})
        board_topic_url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'href = "{0}"'.format(board_topic_url))
