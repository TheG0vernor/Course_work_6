from rest_framework import serializers

from ads.models import Ad, Comment


# TODO Сериалайзеры. Предлагаем Вам такую структуру, однако вы вправе использовать свою

class CommentSerializer(serializers.ModelSerializer):
    # TODO сериалайзер для модели
    model = Comment
    fields = '__all__'


class AdSerializer(serializers.ModelSerializer):
    # TODO сериалайзер для модели
    model = Ad
    fields = '__all__'


class AdDetailSerializer(serializers.ModelSerializer):
    # TODO сериалайзер для модели
    author_id = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )
    author_first_name = serializers.SlugRelatedField(
        read_only=True,
        slug_field='first_name',
    )
    author_last_name = serializers.SlugRelatedField(
        read_only=True,
        slug_field='last_name',
    )

    model = Ad
    exclude = ['id', 'author']
