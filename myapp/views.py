from django.shortcuts import render, HttpResponse
from .models import *


def article_list(request):
    article = Student.objects.all()
    return render(request, "myapp/index.html", {"article": article})

