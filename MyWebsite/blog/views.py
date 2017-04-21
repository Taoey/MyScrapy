from django.shortcuts import render
from django.http import HttpResponse

from selenium import webdriver
from lxml import etree
import time,random

from . import models
from .tools.addForm import People
# Create your views here.
#
# def index(request):
#
#     peoples=models.People.objects.all()
#     return render(request,'blog/index.html',{'peoples':peoples})



def index(request):
    if request.method == 'POST':  # 当提交表单时

        form = People(request.POST)  # form 包含提交的数据

        if form.is_valid():  # 如果提交的数据合法
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']
            peoples = models.People.objects.filter(name=a)
            return render(request, 'blog/index.html', {'peoples': peoples})
    return render(request, 'blog/index.html',)




def getdata(request):
    chromedriver = "D:\CCApplication\phantomjs-2.1.1-windows\bin\phantomjs.exe"
    driver = webdriver.PhantomJS()
    if request.method == 'POST':  # 当提交表单
        url=request.POST['a']
        driver.get("https://{}".format(url))
    webdata=driver.page_source
    driver.quit()

    return  render(request, 'blog/index.html', {'result':webdata})














