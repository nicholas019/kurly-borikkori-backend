from django.db import models

from core.models     import TimeStampedModel

from products.models import Product
from users.models    import User


class Menu(models.Model):
    name = models.CharField(max_length=45)
    
    class Meta:
        db_table = 'menus'


class MainCategory(models.Model):
    name = models.CharField(max_length=45)
    
    class Meta:
        db_table = 'main_categories'


class SubCategory(models.Model):
    name          = models.CharField(max_length=45)

    class Meta:
        db_table = 'sub_categories'


class Recipe(TimeStampedModel):
    title         = models.CharField(max_length=45)
    intro         = models.TextField()
    thumbnail     = models.CharField(max_length=150)
    cooktime      = models.IntegerField()
    serving       = models.IntegerField()
    hit           = models.IntegerField()
    difficulty    = models.CharField(max_length=45)
    menu          = models.ForeignKey('Menu', on_delete=models.CASCADE)
    main_category = models.ForeignKey('MainCategory', on_delete=models.CASCADE)
    sub_category  = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
    user          = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'recipes'


class RecipeProduct(models.Model):
    recipe   = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'recipe_product'



class Ingredient(models.Model):
    name     = models.CharField(max_length=45)
    quantity = models.CharField(max_length=100)
    recipe   = models.ForeignKey('Recipe', on_delete=models.CASCADE)

    class Meta:
        db_table = 'ingredients'


class Content(models.Model):
    step    = models.IntegerField()
    content = models.CharField(max_length=100)
    recipe  = models.ForeignKey('Recipe', on_delete=models.CASCADE)

    class Meta:
        db_table = 'contents'


class ContentImage(models.Model):
    image = models.CharField(max_length=150)
    content = models.ForeignKey('Content', on_delete=models.CASCADE)

    class Meta:
        db_table = 'content_images'


class RecipeLike(models.Model):
    user   = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)

    class Meta:
        db_table = 'recipe_like'


class RecipeComment(TimeStampedModel):
    content        = models.CharField(max_length=200)
    tag            = models.BooleanField()
    user           = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe         = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'recipe_comments'


class RecipeCommentLike(models.Model):
    user           = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_comment = models.ForeignKey('RecipeComment', on_delete=models.CASCADE)

    class Meta:
        db_table = 'recipecomment_like'

class HashTag(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'hash_tags'

class RecipeHashTag(models.Model):
    recipe   = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    hash_tag = models.ForeignKey('HashTag', on_delete=models.CASCADE)

    class Meta:
        db_table = 'recipe_hash_tags'

