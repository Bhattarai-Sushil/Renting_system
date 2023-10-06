from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
     path('login', views.user_login, name='login'),
    path('register', views.register, name='register'),
    path('logout',views.logout_user,name='logout'),
    path('postad',views.postad,name='postad'),

    path('flats/<slug:slugs>/<int:id>',views.adDetail,name="flats"),
]