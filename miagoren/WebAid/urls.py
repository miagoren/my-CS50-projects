from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    re_path(r'^opportunities/', views.opportunities, name='opportunities'),
    path('create', views.create, name='create'),
    path('opportunity/<int:opportunity_id>', views.opportunity, name='opportunity'),
    path('user/<int:user_id>', views.user, name='user'),
    re_path(r'^messaging/', views.messaging, name='messaging'),
    path('search', views.search, name='search'),
    re_path(r'^helpers/', views.helpers, name='helpers')
]
