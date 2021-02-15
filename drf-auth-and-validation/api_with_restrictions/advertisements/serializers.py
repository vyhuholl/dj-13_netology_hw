from django.contrib.auth.models import User
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement, Favourites


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        ads = Advertisement.objects.select_related().filter(
            creator__username=self.context['request'].user,
            status='OPEN'
        )
        if len(ads) == 10:
            raise ValidationError(
        {'error': 'One user can have no more than 10 open ads!'}
        )
        return data


class FavouritesSerializer(serializers.ModelSerializer):
    """Serializer для избранного объявления."""

    class Meta:
        model = Favourites
        fields = ('advertisement',)

    def create(self, validated_data):
        """Метод для создания"""

        validated_data['user_id'] = self.context['request'].user.id
        return super().create(validated_data)

    def validate(self, attrs):
        """Метод для валидации. Вызывается при создании и обновлении."""

        if self.context['request'].user == attrs['advertisement'].creator:
            raise ValidationError(
        {'error': 'Your own ads cannot be in favourites.'}
        )
        return attrs
