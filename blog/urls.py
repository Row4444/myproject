from django.urls import path, include

from blog.views import PostCreate, PostList, PostDetailAndComment

urlpatterns = [
                  path('add/post', PostCreate.as_view(), name='Create'),
                  path('', PostList.as_view(), name='Posts'),
                  path('<int:id>/', PostDetailAndComment.as_view(), name='post_detail_url'),
              ]
