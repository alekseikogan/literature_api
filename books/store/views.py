from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.permissions import IsAuthenticated
from .models import Book
from .permissions import IsOwnerOrStaffOrReadOnly
from .serializers import BookSerializer, UserBookRelationSerializer
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .models import UserBookRelation


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['price']
    search_fields = ['title', 'author']
    ordering_fields = ['price', 'author']

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


def auth(request):
    return render(request, 'oauth2.html')


class UserBooksRelationView(mixins.UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    lookup_field = 'book'  # для удобства

    def get_object(self):
        obj, _ = UserBookRelation.objects.get_or_create(
            user=self.request.user,
            book_id=self.kwargs['book']  # этот book пришел через lookup_field, по сути это id
        )

        return obj
