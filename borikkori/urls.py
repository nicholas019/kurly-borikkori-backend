from django.urls import path, include

urlpatterns = [
    path("user", include('users.urls')),
    path("recipe", include('recipes.urls')),
    path("tip", include('tips.urls')),
    path("product", include('products.urls')),
]
