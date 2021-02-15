from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from permissions import IsAdminOrOwner
from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, Favourites
from advertisements.serializers import FavouritesSerializer
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action == 'create':
            return [IsAuthenticated(),]
        if self.action in ["destroy", "update", "partial_update"]:
            return [IsAuthenticated(), IsAdminOrOwner()]
        return []

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Advertisement.objects.filter(status__in=['OPEN', 'CLOSED'])
        if self.request.user.is_authenticated:
            draft = Advertisement.objects.filter(
                status='DRAFT', creator=self.request.user
                ).order_by('-updated_at', '-created_at')
            return queryset | draft
        return queryset


class FavouritesViewSet(ModelViewSet):
    """ViewSet для избранных объявлений."""

    serializer_class = AdvertisementSerializer

    filter_backends = [DjangoFilterBackend]

    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        ad = Favourites.objects.get(
            user=request.user, advertisement_id=kwargs['pk']
            )
        self.perform_destroy(ad)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        return Favourites.objects.filter(user=self.request.user)
