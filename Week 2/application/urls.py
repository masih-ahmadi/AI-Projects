from django.urls import path
from . import views
from .views import get_story


urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout_user, name="logout"),
    path('profile/', views.profile_user, name="profile_user"),
    

    path('add_story/', views.add_story, name="add_story"),
    path('read_story/<int:id>/', views.read_story, name="read_story"),
    path('api/', get_story, name='get_story')
]
