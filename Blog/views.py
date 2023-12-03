from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Post, Comment
from .serializer import PostSerializer, CommentSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi

class PostList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_description="Get a list of posts",
        responses={200: openapi.Response('List of posts', PostSerializer(many=True))}
    )
    def get(self, request, format=None):
        post = Post.objects.all()
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new post",
        request_body=PostSerializer,
        responses={201: 'Created', 400: 'Bad Request'}
    )

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_description="Get details of a specific post",
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Post ID", type=openapi.TYPE_INTEGER),
        ],
        responses={200: openapi.Response('Post details', PostSerializer)}
    )

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update details of a specific post",
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Post ID", type=openapi.TYPE_INTEGER),
        ],
        request_body=PostSerializer,
        responses={200: 'Updated', 400: 'Bad Request'}
    )

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a specific post",
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Post ID", type=openapi.TYPE_INTEGER),
        ],
        responses={204: 'No Content'}
    )

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_description="Get a list of comments",
        responses={200: openapi.Response('List of comments', CommentSerializer(many=True))}
    )

    def get(self, request, format=None):
        comment = Comment.objects.all()
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new comment",
        request_body=CommentSerializer,
        responses={201: 'Created', 400: 'Bad Request'}
    )

    def post(self, request, format=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_description="Get details of a specific comment",
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Comment ID", type=openapi.TYPE_INTEGER),
        ],
        responses={200: openapi.Response('Comment details', CommentSerializer)}
    )

    def get(self, request, pk, format=None):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update details of a specific comment",
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Comment ID", type=openapi.TYPE_INTEGER),
        ],
        request_body=CommentSerializer,
        responses={200: 'Updated', 400: 'Bad Request'}

    )

    def put(self, request, pk, format=None):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a specific comment",
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Comment ID", type=openapi.TYPE_INTEGER),
        ],
        responses={204: 'No Content'}
    )

    def delete(self, request, pk, format=None):
        comment = self.get_object(pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


