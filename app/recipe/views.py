"""Recipe views module."""

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Recipe
from recipe import serializers
# from django.shortcuts import render

# Create your views here.


class RecipeViewSet(viewsets.ModelViewSet):
    """View for managing recipe APIs."""

    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the recipes for the authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by("-id")

    def get_serializer_class(self):
        """Return appropriate serializer class based on action."""
        if self.action == "retrieve":
            return serializers.RecipeSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)
class TagViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        """Retrieve the tags for the authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by("-id")
