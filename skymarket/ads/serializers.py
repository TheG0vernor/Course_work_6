from rest_framework import serializers

from ads.models import Ad, Comment


class CommentSerializer(serializers.ModelSerializer):
    model = Comment
    fields = '__all__'


class AdSerializer(serializers.ModelSerializer):
    model = Ad
    fields = '__all__'


class AdDetailSerializer(serializers.ModelSerializer):
    pk = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
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
