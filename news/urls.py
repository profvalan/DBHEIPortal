from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    # Public
    path('', views.news_list, name='list'),
    path('article/<slug:slug>/', views.news_detail, name='detail'),
    path('sdg/<int:number>/', views.sdg_news, name='sdg_news'),

    # Institution dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('my-news/', views.my_news, name='my_news'),
    path('create/', views.news_create, name='create'),
    path('edit/<int:pk>/', views.news_edit, name='edit'),
    path('delete/<int:pk>/', views.news_delete, name='delete'),

    # Admin
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/review/<int:pk>/', views.admin_review, name='admin_review'),
    path('admin/all/', views.admin_all_news, name='admin_all_news'),

    # REST API
    path('api/news/', views.api_news_list, name='api_list'),
    path('api/news/<slug:slug>/', views.api_news_detail, name='api_detail'),
]
