from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from main.models import Article


class HomeView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        articles = Article.objects.all().order_by('-created_at')
        user = request.user
        context = {'articles': articles,
                   'user': user
                   }
        return render(request, 'home.html', context)


class ArticleDetailsView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        context = {'article': article}
        return render(request, 'detail-page.html', context)


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return redirect('register')
        if User.objects.filter(username=username).exists():
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('home')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        return redirect('login')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class MyArticlesView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        articles = Article.objects.filter(author=request.user)
        context = {'articles': articles}
        return render(request, 'myarticles.html', context)

class ArticleEditView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug, author=request.user)
        context = {'article': article}
        return render(request, 'edit.html', context)

    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug, author=request.user)
        article.title = request.POST.get('title')
        article.content = request.POST.get('content')
        tag_ids = request.POST.getlist('tags')
        article.tags.set(tag_ids)
        article.save()
        return redirect('article_details', slug=article.slug)


class ArticleDeleteView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug, author=request.user)
        context = {'article': article}
        return render(request, 'delete.html', context)

    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug, author=request.user)
        article.delete()
        return redirect('home')