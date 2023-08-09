from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[

   path("blogs",views.blog,name="blog"),
   path("blog_details/<int:post_id>",views.blog_post,name="blog_details"),
   path("comment",views.comments,name="comment"),
   path("search", views.search_tag, name='search'),
   ] 