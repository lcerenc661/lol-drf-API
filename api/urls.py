"""Urls mapppings for the recipe app."""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register('champions', views.ChampionViewSet, basename='champions')

urlpatterns = [
    path('', include(router.urls)),

]
