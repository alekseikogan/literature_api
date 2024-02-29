from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from store.views import UserBooksRelationView

from store.views import BookViewSet, auth

router = routers.DefaultRouter()
router.register(r'book', BookViewSet)
router.register(r'book_relation', UserBooksRelationView)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('', include('social_django.urls', namespace='social')),
    path('auth/', auth),
]

urlpatterns += router.urls
