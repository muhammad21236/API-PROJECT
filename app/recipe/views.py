"""Recipe views module."""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Recipe
from recipe import serializers
# from django.shortcuts import render

# Create your views here.


class RecipeViewSet(viewsets.ModelViewSet):
    """View for managing recipe APIs."""

    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the recipes for the authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by("-id")

    # def perform_create(self, serializer):
    #     """Create a new recipe."""
    #     serializer.save(user=self.request.user)
    # def perform_update(self, serializer):
    #     """Update an existing recipe."""
    #     serializer.save(user=self.request.user)
    # def perform_destroy(self, instance):
    #     """Delete an existing recipe."""
    #     instance.delete()
    # def list(self, request, *args, **kwargs):
    #     """List all recipes."""
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return render(request, 'recipe/recipe_list.html', {'recipes': serializer.data})
    # def retrieve(self, request, *args, **kwargs):
    #     """Retrieve a recipe by ID."""
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return render(request, 'recipe/recipe_detail.html', {'recipe': serializer.data})
    # def create(self, request, *args, **kwargs):
    #     """Create a new recipe."""
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     return render(request, 'recipe/recipe_detail.html', {'recipe': serializer.data})
    # def update(self, request, *args, **kwargs):
    #     """Update an existing recipe."""
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return render(request, 'recipe/recipe_detail.html', {'recipe': serializer.data})
    # def destroy(self, request, *args, **kwargs):
    #     """Delete an existing recipe."""
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return render(request, 'recipe/recipe_list.html', {'message': 'Recipe deleted successfully'})
