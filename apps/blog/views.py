from collections.abc import Generator

from django.template.defaulttags import comment
from rest_framework import viewsets, generics, status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.blog.models import Blog, Category, Comments
from apps.blog.serializers import BlogSerializer, CategorySerializer, CommentSerializer
from apps.common.permissions import ReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class BlogListView(GenericAPIView):
    serializer_class = BlogSerializer
    permission_classes = (ReadOnly,)

    def get(self, request: Request) -> Response:
        blogs = Blog.objects.all()
        return Response(self.get_serializer(blogs, many=True).data)


class BlogItemView(GenericAPIView):
    serializer_class = BlogSerializer
    permission_classes = (ReadOnly, IsAuthenticated)

    def get(self, request: Request, pk: int) -> Response:
        blog: Blog = get_object_or_404(Blog.objects.all(), pk=pk)
        return Response(self.get_serializer(blog).data)


class BlogCreateView(generics.CreateAPIView):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()

class BlogDetailView(APIView):
    def get(self, request, id):
        try:
            blog = Blog.objects.get(id=id)
            comments = Comments.objects.filter(blog=blog)
            blog_data = BlogSerializer(blog).data
            comments_data = CommentSerializer(comments, many=True).data
            return Response({
                'blog': blog_data,
                'comments': comments_data
            }, status=status.HTTP_200_OK)
        except Blog.DoesNotExist:
            return Response({'error': 'Blog not found!'}, status=status.HTTP_404_NOT_FOUND)

class CommentCreateView(APIView):
    def post(self, request, *args, **kwargs):
        blog_id = request.data.get('blog_id')
        text = request.data.get('text')

        comment = Comments.objects.create(blog=blog_id, text=text)
        serializer = CommentSerializer(comment)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
