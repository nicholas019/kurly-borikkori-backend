from django.db import models

from core.models import TimeStampedModel
from recipes.models import Menu, Recipe
from users.models import User

class Review(TimeStampedModel):
    title      = models.CharField(max_length=45)
    content    = models.TextField()
    thumbnaiul = models.CharField(max_length=150)
    hit        = models.IntegerField()
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe     = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True)
    menu       = models.ForeignKey(Menu, on_delete=models.CASCADE)

    class Meta:
        db_table = 'reviews'


class ReviewLike(models.Model):
    user   = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey('Review', on_delete=models.CASCADE)

    class Meta:
        db_table = 'review_like'


class ReviewComment(TimeStampedModel):
    content        = models.CharField(max_length=200)
    tag            = models.CharField(max_length=30)
    user           = models.ForeignKey(User, on_delete=models.CASCADE)
    review         = models.ForeignKey('Review', on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'review_comments'


class ReviewCommentLike(models.Model):
    user           = models.ForeignKey(User, on_delete=models.CASCADE)
    reveiw_comment = models.ForeignKey('ReviewComment', on_delete=models.CASCADE)

    class Meta:
        db_table = 'rviewcomment_like'
