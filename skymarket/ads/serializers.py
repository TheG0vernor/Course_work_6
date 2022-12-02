from rest_framework import serializers

from ads.models import Ad, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class AdDetailSerializer(serializers.ModelSerializer):
    pk = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    author_id = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )
    author_first_name = serializers.SerializerMethodField()
    author_last_name = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    @staticmethod
    def get_author_first_name(ad):
        return ad.author.first_name
    @staticmethod
    def get_author_last_name(ad):
        return ad.author.last_name
    @staticmethod
    def get_phone(ad):
        return str(ad.author.phone)

    class Meta:
        model = Ad
        fields = ['pk', 'author_id', 'author_first_name', 'author_last_name',
                  'image', 'title', 'price', 'phone', 'description']

