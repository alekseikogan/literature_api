from rest_framework import serializers

from .models import Book, UserBookRelation


class BookSerializer(serializers.ModelSerializer):

    likes_count = serializers.SerializerMethodField()
    # annotated_likes = serializers.IntegerField(read_only=True)
    # rating = serializers.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        model = Book
        fields = ('id', 'title', 'price', 'author', 'rating',)

    # def get_likes_count(self, instance):
    #     return UserBookRelation.objects.filter(book=instance, like=True).count()


class UserBookRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'like', 'in_bookmarks', 'rate')
