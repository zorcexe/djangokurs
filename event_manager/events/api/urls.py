from django.urls import path
from .views import CategoryListCreateApiView, CategoryRetrieveAPiView

app_name = "events_api"

urlpatterns = [
    # api/events/categories
    path(
        "categories",
        CategoryListCreateApiView.as_view(),
        name="categories",
    ),
    path(
        "categories/<int:pk>",
        CategoryRetrieveAPiView.as_view(),
        name="category_detail",
    ),
]
