from django.urls import include,path
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("index/", views.IndexView.as_view(), name="index"),
    path("detail/<str:pk>/", views.DetailView.as_view(), name="detail"),
    path('add/', views.addMovie, name='addMovie'),

]
