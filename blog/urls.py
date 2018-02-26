from django.conf.urls import url
from blog import views
from .views import PostListView, PostDetailView, CreatePostView, PostUpdateView, PostDeleteView, \
                   DraftListView, add_comment_to_post, comment_approve, comment_remove, post_publish


urlpatterns = [
    url(r'^$',PostListView.as_view(),name='post_list'),
    url(r'^post/(?P<slug>[\w-]+)$',PostDetailView.as_view(),name='post_detail'),
    url(r'^post/new/$',CreatePostView.as_view(),name='post_new'),
    url(r'^post/(?P<slug>[\w-]+)/edit/$',PostUpdateView.as_view(),name='post_edit'),
    url(r'^post/(?P<slug>[\w-]+)/remove/$',PostDeleteView.as_view(),name='post_remove'),
    url(r'^drafts/$',DraftListView.as_view(),name='post_draft_list'),
    url(r'^post/(?P<slug>[\w-]+)/comment/$',add_comment_to_post,name='add_comment_to_post'),
    url(r'^comment/(?P<pk>\d+)/approve/$',comment_approve,name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$',comment_remove,name='comment_remove'),
    url(r'^post/(?P<slug>[\w-]+)/publish/$',post_publish,name='post_publish'),



]
