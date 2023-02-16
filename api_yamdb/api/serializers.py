from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений (только для чтения)"""
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(default=1)

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений (для записи)."""
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()

    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов (только для редактирования)."""
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)


class ReviewSerializer(ReviewUpdateSerializer):
    """Сериализатор для отзывов (кроме редактирования)."""
    def validate(self, data):
        request = self.context['request']
        author_id = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        if Review.objects.filter(
            author=author_id, title=title_id
        ).exists():
            raise serializers.ValidationError(
                'Каждый пользователь может оставить только один отзыв '
                'к произведению'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)


class SendCodeSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации."""
    class Meta:
        model = User
        fields = ('username', 'email',)


class CheckConfirmationCodeSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей."""
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role',
        )
