from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title
from users.models import User

from .filters import FilterForTitle
from .mixins import CLDViewSet
from .permissions import (
    IsAdminOrReadOnly,
    IsAuthorOrModeratorOrAdminOrReadOnly,
    IsSuperUserOrAdmin
)
from .serializers import (
    CategorySerializer,
    CheckConfirmationCodeSerializer,
    CommentSerializer,
    GenreSerializer,
    ReadOnlyTitleSerializer,
    ReviewSerializer,
    ReviewUpdateSerializer,
    SendCodeSerializer,
    TitleSerializer,
    UserSerializer
)


class CategoryViewSet(CLDViewSet):
    """Представление для категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CLDViewSet):
    """Представление для жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Представление для произведений."""
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    )
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilterForTitle

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ReadOnlyTitleSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление для отзывов."""

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return ReviewUpdateSerializer
        return ReviewSerializer

    def get_permissions(self):
        if self.action in ('partial_update', 'destroy',):
            return (IsAuthorOrModeratorOrAdminOrReadOnly(),)
        if self.action == 'create':
            return (permissions.IsAuthenticated(),)
        return super().get_permissions()

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Представление для комментариев к отзывам."""
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action not in ('list', 'retrieve',):
            return (IsAuthorOrModeratorOrAdminOrReadOnly(),)
        return super().get_permissions()

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id', 'title__id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review, pk=self.kwargs.get('review_id', 'title__id')
        )
        serializer.save(author=self.request.user, review=review)


@api_view(('POST',))
def sign_up(request):
    """Представление для регистрации."""
    serializer = SendCodeSerializer(data=request.data)
    email = request.data.get('email')
    username = request.data.get('username')

    if User.objects.filter(username=username, email=email).exists():
        return Response(
            serializer.initial_data, status=status.HTTP_200_OK
        )

    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = User.objects.get(username=request.data.get('username'))
    confirmation_code = default_token_generator.make_token(user)

    mail_subject = 'Код подтверждения на Yamdb.ru'
    message = f'Ваш код подтверждения: {confirmation_code}'
    send_mail(
        mail_subject, message, settings.EMAIL_HOST_USER, [email]
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(('POST',))
def get_jwt_token(request):
    """Представление для получения токена."""
    serializer = CheckConfirmationCodeSerializer(data=request.data)
    confirmation_code = request.data.get('confirmation_code')

    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data['username']
    )
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response(
            {'token': f'{token}'}, status=status.HTTP_200_OK
        )
    return Response(
        serializer.errors, status=status.HTTP_400_BAD_REQUEST
    )


class UserViewSet(viewsets.ModelViewSet):
    """Представление для пользователей."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsSuperUserOrAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'delete', 'patch',)

    @action(
        methods=('get', 'patch',),
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        """Обработка url users/me/."""
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                user, partial=True, data=request.data
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
