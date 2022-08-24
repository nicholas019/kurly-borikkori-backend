from django.urls import path

from users.views import UserInfo, UserBestList, UserRecipeWrite, UserReviewWrite

urlpatterns = [
    path("/<int:id>/info", UserInfo.as_view()),
    path("/<int:id>/wreview", UserReviewWrite.as_view()),
    path("/<int:id>/wrecipe", UserRecipeWrite.as_view()),
    path("/list", UserBestList.as_view())
]
