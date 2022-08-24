from django.urls import path

from products.views import ProductList

urlpatterns = [
    path("/list", ProductList.as_view()),
]
