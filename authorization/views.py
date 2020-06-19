from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse, JsonResponse
from . import forms,models
from api.models import Library,Article
from django.conf import settings
from django.contrib.auth import login,logout,authenticate
from frontend.reccom import get_similar_items
# Create your views here.


def sign_up(request):
    if request.method == "POST":
        form = forms.Signup(request.POST)
        if form.is_valid():
            print(dict(form.cleaned_data))
            form.save()


            user = authenticate(request,username=form.cleaned_data["email"],password=form.cleaned_data["password1"])
            library = Library(name="Reading list",user=user)
            library.save()

            login(request,user)
            return redirect(reverse('questions'))
        return render(request,"auth/signup.html",{"form":form})

    form = forms.Signup()
    return render(request,"auth/signup.html",{"form":form})

def signup_questions(request):
    if request.user.is_authenticated:
        print(request.user)
        return render(request,"auth/questions.html",{"disciplines":settings.SUBDISCIPLINES})

    return HttpResponse("NOT ALLOWED")

def login_(request):
    if request.user.is_authenticated:
        return redirect(reverse("home"))
    if request.method == "POST":
        form = forms.Login(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request,username=email,password=password)
            if not user:
                form = forms.Login()
                return render(request,'login.html',{'form':form,'error':'Passsword incorrect'})
            login(request,user)
            return redirect(reverse("home"))

        return render(request,'auth/login.html',{'form':form})

    form = forms.Login()
    return render(request,'auth/login.html',{'form':form})


def logout_(request):
    logout(request)
    return redirect(reverse("home"))

def get_recommendation_user(request):
    arts = []
    if request.user.keywords:
        for i in request.user.keywords:
            ids = get_similar_items(query=i,start=0,end=100)
            arts.extend(ids)
    if request.user.tags:
        for i in request.user.tags:
            ids = get_similar_items(query=i,start=0,end=100)
            arts.extend(ids)
    arts = set(arts)
    res = [{'title':i.title,'id':i.pk} for i in Article.objects.filter(pk__in = list(arts))]
    return JsonResponse(res,safe=False)
    # return arts
