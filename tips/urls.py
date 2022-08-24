from django.urls import path

from tips.views import TipListView

urlpatterns = [
    path("/list", TipListView.as_view()),
]
