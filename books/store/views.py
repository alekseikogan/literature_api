from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.permissions import IsAuthenticated
from .models import Book
from .permissions import IsOwnerOrStaffOrReadOnly
from .serializers import BookSerializer, UserBookRelationSerializer
from rest_framework import mixins

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


class UserBooksRelationView(mixins.UpdateModelMixin, mixins.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    lookup_field = 'book'

