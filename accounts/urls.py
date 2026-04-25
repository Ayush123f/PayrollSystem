from django.urls import path
from . import views

urlpatterns = [
    path('login/',           views.CustomLoginView.as_view(),  name='login'),
    path('logout/',          views.CustomLogoutView.as_view(), name='logout'),
    path('profile/',         views.profile,                    name='profile'),
    path('change-password/', views.change_password,            name='change_password'),
]