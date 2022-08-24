import json, boto3

from django.views import View
from django.http import JsonResponse
from django.db.models import Q
from django.db import transaction
from django.conf import settings

from recipes.models import Content, ContentImage, HashTag, Ingredient, Recipe, RecipeComment, RecipeProduct, RecipeLike, RecipeCommentLike

from utils.fileuploader_api import FileUploader, FileHandler
from utils.login_decorator import login_decorator
from utils.word_extract import word_extract
from utils.ip_get_modul import get_client_ip

config = {
    "bucket" : settings.AWS_STORAGE_BUCKET_NAME
}

file_uploader = FileUploader(boto3.client('s3'), config)
file_handler = FileHandler(file_uploader)


class RecipeListView(View):
    def get(self, request, menu_id):
        tag    = int(request.GET.get('tag',1))
        main   = int(request.GET.get('main', 1))
        sub    = int(request.GET.get('sub', 1))
        sort   = int(request.GET.get('sort', 1))
        search = request.GET.get('search')

        if sort > 4:
            sort_set = {
                1 : "-id",
                2 : "-hit",
                3 : "-recipelike__recipe_id",
            }
            recipe_list = Recipe.objects.filter(menu_id = menu_id).select_related('user').order_by(sort_set[sort])
        else:
            recipe_list = Recipe.objects.filter(menu_id = menu_id).select_related('user').order_by("-hit", "-recipelike__recipe_id")
        
        q = Q()
        
        if main == 1:
            q = Q()
            if sub > 1:
                q = Q(sub_category_id = sub)
        elif main > 1 :
            q = Q(main_category_id = main)
            if sub > 1:
                q = Q(main_category_id = main) & Q(sub_category_id = sub)

        recipe_list = recipe_list.filter(q)    

        if search:
            q = Q()
            if tag == 1:
                q &= Q(title__icontains = search)
            elif tag == 2:
                q &= Q(content__content__icontains=search)|\
                    Q(hashtag__name__icontains=search)|\
                    Q(intro__country__icontains=search)
            elif tag == 3:
                q &= Q(title__icontains=search)|\
                    Q(content__content__icontains=search)|\
                    Q(hashtag__name__icontains=search)|\
                    Q(intro__country__icontains=search)   
            elif tag == 4:
                q &= Q(user__name__icontains=search)   
            
            recipe_list = recipe_list.filter(q)

        result = [{
            "id"               : recipe.id,
            "title"            : recipe.title,
            "recipe_thumbnail" : recipe.thumbnail,
            "intro"            : recipe.intro,
            "user_id"          : recipe.user.id,
            "user_thumbnauil"  : recipe.user.thumbnail,
            "user_name"        : recipe.user.name,
            "rating_id"        : recipe.user.rating_id,
            "rating_name"      : recipe.user.rating.name,
            "rating_mark_image": recipe.user.rating.mark_image,
            "hit"              : recipe.hit,
            "like_count"       : recipe.recipelike_set.all().count(),
            "comment_count"    : recipe.recipecomment_set.all().count()
        }for recipe in recipe_list]

        return JsonResponse({"result": result}, status = 200)

class RecipeWrite(View):
    @login_decorator
    def post(self, request, menu_id):
        title          = request.POST.get("title")
        intro          = request.POST.get("intro")
        thumbnail      = request.FILES.get("thumbnail")
        user_id        = request.user.id
        cooktime       = request.POST.get("cooktime")
        serving        = request.POST.get("serving")
        difficulty     = request.POST.get("difficulty")
        main_key       = request.POST.get("main_category_id")
        sub_key        = request.POST.get("sub_category_id")
        ingredients    = request.POST["ingredient"]
        products       = request.POST["product"]
        contents       = request.POST["content"]
        content_images = request.FILES.getlist("content_image")
        hash_tag       = request.POST.getlist("hash_tag")

        ingredients = json.loads(ingredients)
        products = json.loads(products)
        contents = json.loads(contents)

        extension = ['PNG', 'png','jpg', 'JPG', 'GIF', 'gif', 'JPEG', 'jpeg']
        if not str(thumbnail).split('.')[-1] in extension:
            return JsonResponse({"message":"INVALID EXTENSION"}, status = 400)
        
        thumbnail_url = file_handler.upload(file=thumbnail)    
        
        main_category_set = {
            "전체보기": 1,
            "한식"  : 2,
            "중식"  : 3,
            "일식"  : 4,
            "양식"  : 5,
            "그외"  : 6
        } 
        sub_category_set = {
            "전체보기": 1,
            "메인요리": 2,
            "밑반찬" : 3,
            "간식"  : 4,
            "안주"  : 5
        } 

        with transaction.atomic():
            recipe = Recipe.objects.create(
                title           = title,
                intro           = intro,
                thumbnail       = thumbnail_url,
                user_id         = user_id,
                cooktime        = cooktime,
                serving         = serving,
                difficulty      = difficulty,
                hit             = 0,
                menu_id = menu_id,
                main_category_id= main_category_set[main_key],
                sub_category_id = sub_category_set[sub_key]
            )

            ingredient_list = [Ingredient(name = i["name"], quantity = i["quantity"], recipe_id = recipe.id)for i in ingredients]

            product_list = [RecipeProduct(product_id = i["id"], recipe_id = recipe.id)for i in products ]    
            
            hashtag_list = [HashTag(name=i) for i in hash_tag ]
            
            
            Ingredient.objects.bulk_create(ingredient_list)
            RecipeProduct.objects.bulk_create(product_list)
            HashTag.objects.bulk_create(hashtag_list)

        content_image_list = []
        for image in content_images:
            extension = ['PNG', 'png','jpg', 'JPG', 'GIF', 'gif', 'JPEG', 'jpeg']
            if not str(image).split('.')[-1] in extension:
                return JsonResponse({"message":"INVALID EXTENSION"}, status = 400)
            image_url = file_handler.upload(file=image)    
            content_image_list.append(image_url)

        for i in range(len(content_image_list)):
            with transaction.atomic():
                content=Content.objects.create(
                    step      = contents[i]["step"],
                    content   = contents[i]["content"],
                    recipe_id = recipe.id
                    )
                ContentImage.objects.create(
                    image      = content_image_list[i],
                    content_id = content.id
                    )   

        return JsonResponse({"message": "SUCCESS"}, status = 200)

class RecipeDetailView(View):
    def get(self, request, id):
        recipe = Recipe.objects.get(id = id)

        result = {
            "id"               : recipe.id,
            "tilte"            : recipe.title,
            "intro"            : recipe.intro,
            "thumbnail"        : recipe.thumbnail,
            "hit"              : recipe.hit,
            "like_count"       : recipe.recipelike_set.all().count(),
            "comment_count"    : recipe.recipecomment_set.all().count(),
            "user_id"          : recipe.user_id,
            "name"             : recipe.user.name,
            "user_thumbnail"   : recipe.user.thumbnail,
            "rating_id"        : recipe.user.rating_id,
            "rating_name"      : recipe.user.rating.name,
            "rating_mark_image": recipe.user.rating.mark_image,
            "cooktime"         : recipe.cooktime,
            "serving"          : recipe.serving,
            "difficulty"       : recipe.difficulty,
            "ingredient"       : [{
                "id"      : ingre.id,
                "name"    : ingre.name,
                "quantity": ingre.quantity
                } for ingre in recipe.ingredient_set.all()],
            "product" : [{
                "id"   : product.product.id,
                "name" : product.product.name,
                "price": product.product.price,
                "image": product.product.image
                } for product in recipe.recipeproduct_set.all()],
            "content"       : [{
                    "id"     : content.id,
                    "step"   : content.step,
                    "content": content.content,
                    "image"  : [i.image for i in content.contentimage_set.all()],
                }for content in recipe.content_set.all()],
            "hash_tag"      : [{
                    "id"  : hash.hashtag.id,
                    "name": hash.hashtag.name
                }for hash in recipe.recipehashtag_set.all()], 
        }
        recipe.hit += 1
        recipe.save()
        return JsonResponse({"result": result}, status = 200)


class RecipeCommnetView(View):
    @login_decorator
    def post(self, request, recipe_id):
        data = json.loads(request.body)

        content = data.get('content')
        tag = data.get('tag')

        RecipeComment.objects.create(
            content           = content,
            tag               = tag,
            user_id           = request.user.id,
            recipe_id         = recipe_id,
            parent_comment_id = None
        )

        return JsonResponse({"message": "SUCCESS"}, status = 200)

    def get(self, request, recipe_id):
        
        recipe_comments = RecipeComment.objects.filter(recipe_id = recipe_id)
        recipe_comments = recipe_comments.filter(parent_comment_id = None)
        recipe_count = len(recipe_comments)
        result = [{         
            "id"                 : comment.id,
            "user_id"            : comment.user_id,
            "user_name"          : comment.user.name,
            "tag"                : comment.tag,
            "content"            : comment.content,
            "created_at"         : comment.created_at,
            "recipe_comment_like": comment.recipecommentlike_set.all().count(),
            "counter"              : comment.parent_comment_id
            }for comment in recipe_comments]
        
        return JsonResponse({"result": result}, status = 200)
    @login_decorator
    def delete(self, request, recipe_id, comment_id):
        RecipeComment.objects.get(recipe_id = recipe_id, id = comment_id).delete()        

        return JsonResponse({"message": "SUCCESS"}, status = 200)
class ReCommentView(View):
    def get(self, request, recipe_id, comment_id):
        recomments = RecipeComment.objects.filter(parent_comment_id = comment_id, recipe_id = recipe_id)

        result = [{         
            "id"               : comment.id,
            "user_id"          : comment.user_id,
            "user_name"        : comment.user.name,
            "tag"              : comment.tag,
            "content"          : comment.content,
            "created_at"       : comment.created_at,
            }for comment in recomments]
        
        return JsonResponse({"result": result}, status = 200)

    @login_decorator
    def post(self,request, recipe_id):
        data = json.loads(request.body)

        content = data.get('content')
        recomment_id = data.get('recomment_id')

        RecipeComment.objects.create(
            content           = content,
            tag               = True,
            user_id           = request.user.id,
            recipe_id         = recipe_id,
            parent_comment_id = recomment_id
        )

        return JsonResponse({"message": "SUCCESS"}, status = 200)


class RecipeSimiltude(View):
    def get(self, request, recipe_id):
        recipe_content = Content.objects.filter(recipe_id = recipe_id)
        
        content = ""
        for i in recipe_content:
            content += i.content
        
        word_rank_list = word_extract(content)[:5]
        recipe_lists = []
        for i in word_rank_list:
            r = Recipe.objects.filter(content__content__icontains = i).first()
            recipe_lists.append(r)
        
        result = [{
            "id"       : recipe.id,
            "title"    : recipe.title,
            "thumbnail": recipe.thumbnail
            }for recipe in recipe_lists]

        return JsonResponse({"result": result}, status = 200)    

class RecipeLikeView(View):
    @login_decorator
    def post(self, request, recipe_id):
        RecipeLike.objects.create(
            user_id   = request.user.id,
            recipe_id = recipe_id
        )
        return JsonResponse({"message": "SUCCESS"}, status = 200)

    @login_decorator
    def delete(self, request, recipe_id):
        try:
            recipe_list = RecipeLike.objects.get(
                user_id   = request.user.id,
                recipe_id = recipe_id
            )
            recipe_list.delete()

            return JsonResponse({"message": "SUCCESS"}, status = 205)
        except RecipeLike.DoesNotExist:
            return JsonResponse({"message" : "DoesNotExist"}, status = 401)  
    
class RecipeCommentLikeView(View):
    @login_decorator
    def post(self, request, recipe_comment_id):
        RecipeCommentLike.objects.create(
            user_id           = request.user.id,
            recipe_comment_id = recipe_comment_id
        )
        return JsonResponse({"message": "SUCCESS"}, status = 200)

    @login_decorator
    def delete(self, request, recipe_comment_id):
        try:
            recipe_list = RecipeCommentLike.objects.get(
                user_id           = request.user.id,
                recipe_comment_id = recipe_comment_id
            )
            recipe_list.delete()

            return JsonResponse({"message": "SUCCESS"}, status = 205)
        except RecipeCommentLike.DoesNotExist:
            return JsonResponse({"message" : "DoesNotExist"}, status = 401)  
    
