from django.contrib import admin
from django.urls import path
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('articles/<slug:slug>/', ArticleDetailsView.as_view(), name='article_details'),
    path('myarticles/', MyArticlesView.as_view(), name='myarticles'),

]
