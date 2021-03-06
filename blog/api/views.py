from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.mixins import DestroyModelMixin
from rest_framework.response import Response
from rest_framework import authentication, permissions

from blog.models import Comment

from .serializers import CommentSerializer

class CommentListAPIView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    def get_queryset(self, *args, **kwargs):
        url = self.request.GET.get("url")
        if url:
            return Comment.objects.filter(url=url)
        return Comment.objects.none()


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        if self.request.user.is_authenticated():
            serializer.save(user=self.request.user)
