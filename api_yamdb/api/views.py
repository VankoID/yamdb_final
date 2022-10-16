from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from reviews.models import Category, Comment, CustomUser, Genre, Review, Title

from .filters import FilterTitle
from .permissions import AdminOnlyOrRead, IsAuthorOrAdminOrModerator
from .serializers import (CategorySerializer, CommentSerializer,
                          CustomUserSerializer, GenreSerializer,
                          ReviewSerializer, TitlePostSerializer,
                          TitleSerializer)


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """Кастомный ViewSet для создания, списка и удаления объектов"""
    pass


class CategoryViewSet(CreateListDestroyViewSet):
    """Кастомный ViewSet для модели Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    permission_classes = (AdminOnlyOrRead,)
    lookup_field = 'slug'
    search_fields = ('name',)


class GenreViewSet(CreateListDestroyViewSet):
    """Кастомный ViewSet для модели Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOnlyOrRead,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    lookup_field = 'slug'
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Title.
    В зависимости от метода запроса возвращает объекты или сериализует их."""
    queryset = Title.objects.all()
    permission_classes = (AdminOnlyOrRead,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilterTitle

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSerializer
        return TitlePostSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Review.
    В случае отсутствия объекта в базе данных возвращает ошибку 404."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrAdminOrModerator,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(title=title, author=self.request.user)

    def perform_update(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        review_id = self.kwargs.get('pk')
        review = get_object_or_404(Review, id=review_id)
        author = review.author
        serializer.save(title_id=title.id, author=author)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Comment.
    В случае отсутствия объекта в базе данных возвращает ошибку 404."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOrModerator,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(review_id=review.id, author=self.request.user)

    def perform_update(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        comment_id = self.kwargs.get('pk')
        comment = get_object_or_404(Comment, id=comment_id)
        author = comment.author
        serializer.save(review_id=review.id, author=author)


class CustomUserViewSet(viewsets.ModelViewSet):
    """ViewSet для модели CustomUser."""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    search_fields = ('username',)
