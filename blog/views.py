from django.shortcuts import render
from  django.http import HttpResponse
from .models import *
def index(request):
    mypost=Blogpost.objects.all()
    return render(request,"blog/index.html" , {'mypost':mypost})

def blogpost(request , id):
    post=Blogpost.objects.filter(post_id=id)[0]
    print(post)
    return render(request,"blog/blogpost.html", {'post': post})