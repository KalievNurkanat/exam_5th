# blog/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, RegisterSerializer
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 67


class PostListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    queryset = Post.objects.all()

    def get(self, request):
        posts = Post.objects.filter(is_published=True) if not request.user.is_authenticated else Post.objects.all()
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(posts, request, view=self)
        serializer = PostSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
       serializer = PostSerializer(data=request.data)
       if serializer.is_valid():
        serializer.save(author=request.user) 
        return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)  
       
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Post.objects.all()
        return Post.objects.filter(is_published=True)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    

class OwnerRights(permissions.BasePermission):
    def permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, OwnerRights]

    def get_object(self, pk):
        return get_object_or_404(Post, pk=pk)

    def get(self, request, pk):
        post = self.get_object(pk)
        if not post.is_published and not request.user.is_authenticated:
            return Response({'detail': 'Authentication required'}, status=status.HTTP_403_FORBIDDEN)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        if post.author != request.user:
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        if post.author != request.user:
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_post(self, post_id):
        return get_object_or_404(Post, pk=post_id)

    def get(self, request, post_id):
        post = self.get_post(post_id)
        comments = post.comments.filter(is_approved=True) if not request.user.is_authenticated else post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, post_id):
        post = self.get_post(post_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



