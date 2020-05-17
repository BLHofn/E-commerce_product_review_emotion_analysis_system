from django.http import HttpResponse
from django.shortcuts import render
from App import models
# Create your views here.
def login(request):
    return render(request, 'login.html')


def grjs(request):
    return render(request, 'grjs.html')


def kysh(request):
    return render(request, 'kysh.html')


def lyb(request):
    return render(request, 'lyb.html')


def sl(request):
    return render(request, 'sl.html')


def tmb(request):
    return render(request, 'tmb.html')


def wlb(request):
    return render(request, 'wlb.html')


def xsh(request):
    return render(request, 'xsh.html')


def xx(request):
    return render(request, 'xx.html')


def xy(request):
    return render(request, 'xy.html')


def zygh(request):
    return render(request, 'zygh.html')


def zz(request):
    return render(request, 'zz.html')


def index(request):
    return render(request, 'index.html')


def mp3(request):
    return render(request, 'mp3.html')

from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
def show(request):
    num=request.GET.get('num',1)
    n=int(num)
    movies=models.JdMdcomments.objects.all()
    pager=Paginator(movies,24)
    try:
        perpage_data=pager.page(n)
    except PageNotAnInteger:
        perpage_data=pager.page(1)
    except EmptyPage:
        perpage_data=pager.page(pager.num_pages)
    return render(request,'kysh.html',{'pager':pager,'perpage_data':perpage_data})
    # data=models.JdMdcomments.objects.all()
    # return render(request,'kysh.html',{'data':data})


def bsxx(request):
    return render(request, 'bsxx.html')