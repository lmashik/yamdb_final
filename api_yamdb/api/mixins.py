from rest_framework import mixins, viewsets


class CLDViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Класс-родитель для представлений категорий и жанров."""
    pass
