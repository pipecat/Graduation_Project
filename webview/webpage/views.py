from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'result.html')

def img1(request):
    imgpath = 'templates/all.png'
    imgdata = open(imgpath, "rb").read()
    return HttpResponse(imgdata, content_type="image/png")

def img2(request):
    imgpath = 'templates/now.png'
    imgdata = open(imgpath, "rb").read()
    return HttpResponse(imgdata, content_type="image/png")

def img3(request):
    imgpath = 'templates/ecnomic.png'
    imgdata = open(imgpath, "rb").read()
    return HttpResponse(imgdata, content_type="image/png")

def img4(request):
    imgpath = 'templates/life.png'
    imgdata = open(imgpath, "rb").read()
    return HttpResponse(imgdata, content_type="image/png")