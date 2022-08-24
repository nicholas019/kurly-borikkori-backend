from django.views import View
from django.http import JsonResponse

from users.models import User
from reviews.models import Review
from recipes.models import Recipe


class UserBestList(View):
    def get(self, request):
        
        user_list = User.objects.filter(is_best = True)

        result = [{
            "id"               : user.id,
            "thumbnail"        : user.thumbnail,
            "name"             : user.name,
            "rating_id"        : user.rating.id,
            "rating_name"      : user.rating.name,
            "rating_mark_image": user.rating.mark_image,
        }for user in user_list]

        return JsonResponse({"result":result}, status = 200)


class UserInfo(View):
    def get(self, request, id):
        user = User.objects.prefetch_related('recipe_set','review_set').\
                select_related('rating').get(id = id)

        result = {
            "id"               : user.id,
            "thumbnail"        : user.thumbnail,
            "name"             : user.name,
            "rating_id"        : user.rating.id,
            "rating_name"      : user.rating.name,
            "rating_mark_image": user.rating.mark_image,
            "recipe_count"     : user.recipe_set.all().count(),
            "review_count"     : user.review_set.all().count(),
        }

        return JsonResponse({"result":result}, status = 200)


class UserReviewWrite(View):
    def get(self, request, id):
        reviews = Review.objects.filter(user_id = id)

        result = [{
            "id"        : review.id,
            "title"     : review.title,
            "content"   : review.content,
            "thumbnail" : review.thumbnail,
            "created_at": review.created_at.strftime("%y.%m.%d"),
        } for review in reviews]

        return JsonResponse({"result": result}, status = 200)

class UserRecipeWrite(View):
    def get(self, request, id):    
        recipes = Recipe.objects.filter(user_id = id)

        result= [{
            "id"        : recipe.id,
            "title"     : recipe.title,
            "intro"     : recipe.intro,
            "thumbnail" : recipe.thumbnail,
            "created_at": recipe.created_at.strftime("%y.%m.%d"),
        } for recipe in recipes]

        return JsonResponse({"result":result}, status = 200)