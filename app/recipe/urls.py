from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views

# Default router automatically generates urls for view set
# /api/recipe/Tags/1/
router = DefaultRouter()
# register view
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]
