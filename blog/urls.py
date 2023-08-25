from django.urls import path,include
from .import views

urlpatterns = [
    path('',views.post_list, name='post_list'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/edit/', views.post_edit, name='post_edit'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>/post_by_categories/', views.category_wise_post, name='category_wise_post'),
    path('tags', views.tags, name='tags'),
    path('tags/<int:pk>/tag_wise_post/', views.tag_wise_post, name='tag_wise_post'),
]