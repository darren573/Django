from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home(request):
    string = '我在自强学堂学习Django，并用它来构建网站'
    return render(request, 'home.html', {'string': string})


def index(request):
    num_list = ["html", "css", "div", "vue", "jQuery"]
    return render(request, 'home.html', {'num_list': num_list})


def second(request):
    info_dict = {'site': "自强学堂", 'content': "各种IT技术"}
    return render(request, 'home.html', {'info_dict': info_dict})


def third(request):
    List = map(str, range(100))
    return render(request, 'home.html', {'List': List})


def add(request):
    a = request.GET['a']
    b = request.GET['b']
    c = int(a) + int(b)
    return HttpResponse(str(c))


def add2(request, a, b):
    c = int(a) + int(b)
    return HttpResponse(str(c))
