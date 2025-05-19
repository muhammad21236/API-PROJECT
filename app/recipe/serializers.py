"""Serializers for recipe APIs."""

from rest_framework import serializers

from core.models import Recipe, Tag

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

class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects."""

    class Meta:
        model = Tag
        fields = ("id", "name")
        read_only_fields = ("id",)