"""Tests for the recipe API endpoints."""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from core.models import Recipe

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer


RECIPIES_URL = reverse("recipe:recipe-list")


def detail_url(recipe_id):
    """Create and return a recipe detail URL."""
    return reverse("recipe:recipe-detail", args=[recipe_id])


def create_recipe(user, **params):
    """Create and return a sample recipe."""
    defaults = {
        "title": "Sample Recipe",
        "time_minutes": 10,
        "price": Decimal("5.00"),
        "link": "http://example.com/recipe.pdf",
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


def create_user(**params):
    """Create and return a sample user."""
    return get_user_model().objects.create_user(**params)


class PublicRecipeAPITests(APITestCase):
    """Test the publicly available recipe API."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required to access the recipe API."""
        res = self.client.get(reverse("recipe:recipe-list"))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Remove duplicate user creation
        self.user = create_user(
            email="user@example.com",
            password="testpass123",
            name="Test User",
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes."""
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPIES_URL)

        recipes = Recipe.objects.all().order_by("-id")
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_limited_to_user(self):
        """Test retrieving recipes for user."""
        other_user = create_user(
            email="other@example.com",
            password="otherpass123",
        )
        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPIES_URL)

        recipes = Recipe.objects.filter(user=self.user).order_by("-id")
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_detail(self):
        """Test get recipe detail."""
        recipe = create_recipe(user=self.user)

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe_successful(self):
        """Test creating a new recipe."""
        payload = {
            "title": "New Recipe",
            "time_minutes": 30,
            "price": Decimal("10.00"),
            "link": "http://example.com/new-recipe.pdf",
        }
        res = self.client.post(RECIPIES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))
        self.assertEqual(recipe.user, self.user)

    def test_partial_update(self):
        """Test Partial Update of a Recipe."""
        original_link = "http://example.com/recipe.pdf"
        recipe = create_recipe(
            user=self.user,
            title="Sample Recipe",
            link=original_link,
        )
        payload = {"title": "Updated Recipe"}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload["title"])
        self.assertEqual(recipe.link, original_link)
        self.assertEqual(recipe.user, self.user)

    def test_full_update(self):
        """Test Full Update of a Recipe."""
        recipe = create_recipe(
            user=self.user,
            title="Sample Recipe",
            link="http://example.com/recipe.pdf",
            description="Sample description",
        )
        payload = {
            "title": "Updated Recipe",
            "time_minutes": 20,
            "price": Decimal("15.00"),
            "link": "http://example.com/updated-recipe.pdf",
        }
        url = detail_url(recipe.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))
        self.assertEqual(recipe.user, self.user)

    def test_update_user_returns_error(self):
        """Test that updating the user field returns an error."""
        new_user = create_user(
            email="user2@example.com",
            password="testpass123",
            name="Test User 2",
        )
        recipe = create_recipe(user=self.user)
        payload = {"user": new_user.id}
        url = detail_url(recipe.id)
        self.client.patch(url, payload)
        recipe.refresh_from_db()
        self.assertEqual(recipe.user, self.user)

    def test_delete_recipe(self):
        """Test deleting a recipe."""
        recipe = create_recipe(user=self.user)
        url = detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        recipes = Recipe.objects.filter(id=recipe.id)
        self.assertFalse(recipes.exists())

    def test_recipe_other_users_recipe_error(self):
        """Test trying to delete another user's recipe gives error."""
        new_user = create_user(
            email="user2@example.com",
            password="testpass123",
            name="Test User 2",
        )
        recipe = create_recipe(user=new_user)
        url = detail_url(recipe.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Recipe.objects.filter(id=recipe.id).exists())
