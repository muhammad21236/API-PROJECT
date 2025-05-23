"""URL mappings for the recipe app."""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter
from recipe import views
from recipe.views import TagViewSet

# Create a router and register our viewset with it.
router = DefaultRouter()
router.register("recipes", views.RecipeViewSet)
router.register("tags", TagViewSet)

app_name = "recipe"
urlpatterns = [
    # The API URLs are now determined automatically by the router.
    path("", include(router.urls)),
]
