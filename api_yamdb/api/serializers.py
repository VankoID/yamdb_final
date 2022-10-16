from django.db.models import Avg
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, CustomUser, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title.
    Обрабатывает объекты GET запросов типа list и retrieve."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField(method_name='get_rating')

    def get_rating(self, title):
        rating = title.reviews.aggregate(rating=Avg('score'))
        if rating:
            return rating['rating']
        return None

    class Meta:
        model = Title
        fields = ('id',
                  'name',
                  'year',
                  'rating',
                  'description',
                  'genre',
                  'category')


class TitlePostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title.
    Обрабатывает объекты POST запросов типа create."""
    genre = SlugRelatedField(
        many=True, queryset=Genre.objects.all(), slug_field='slug'
    )
    category = SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review с кастомным валидатором."""
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        request = self.context.get('request')
        title_id = request.parser_context['kwargs']['title_id']
        title = get_object_or_404(Title, id=title_id)
        if self.context.get(
            'request').method == 'POST' and title.reviews.filter(
                author=request.user).exists():
            raise serializers.ValidationError(
                'Вы уже обозревали это произведение')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели CustomUser."""
    class Meta:
        model = CustomUser
        fields = '__all__'
