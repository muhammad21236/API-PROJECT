"""Serializers for recipe APIs."""

from rest_framework import serializers

from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe objects."""

    class Meta:
        model = Recipe
        fields = ("id", "title", "description", "time_minutes", "price", "link")
        read_only_fields = ("id",)
        extra_kwargs = {
            "description": {"required": False},
            "link": {"required": False},
        }

class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ("description", "link")
        # read_only_fields = RecipeSerializer.Meta.read_only_fields + ("description", "link")
        # recipes = []  # Define or fetch the recipes list here
        # serializer = RecipeSerializer(recipes, many=True)
