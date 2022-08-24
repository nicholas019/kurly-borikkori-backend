from django.urls import path

from recipes.views import ReCommentView, RecipeCommentLikeView, RecipeCommnetView, RecipeDetailView, RecipeLikeView, RecipeListView, RecipeWrite, RecipeSimiltude

urlpatterns = [
    path("/<int:menu_id>/list", RecipeListView.as_view()),
    path("/detail/<int:id>", RecipeDetailView.as_view()),
    path("/detail/<int:recipe_id>/comment", RecipeCommnetView.as_view()),
    path("/detail/<int:recipe_id>/similitube", RecipeSimiltude.as_view()),
    path("/<int:menu_id>/write", RecipeWrite.as_view()),
    path("/detail/<int:recipe_id>/recomment/<int:comment_id>", ReCommentView.as_view()),
    path("/<int:recipe_id>/like", RecipeLikeView.as_view()),
    path("/<int:recipe_id>/comment/<int:recipe_comment_id>/like", RecipeCommentLikeView.as_view()),
]
