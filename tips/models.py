from django.db import models

from core.models import TimeStampedModel

from recipes.models import Menu
from users.models import User
from products.models import Product


class Tip(TimeStampedModel):
    title   = models.CharField(max_length=45)
    content = models.TextField()
    hit     = models.IntegerField()
    image   = models.CharField(max_length=150)
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    menu    = models.ForeignKey(Menu, on_delete=models.CASCADE)

    class Meta:
        db_table = "tips"


class TipComment(TimeStampedModel):
    content        = models.CharField(max_length=200)
    tag            = models.CharField(max_length=30)
    user           = models.ForeignKey(User, on_delete=models.CASCADE)
    tip            = models.ForeignKey('Tip', on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'tip_comments'


class TipLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tip  = models.ForeignKey(Tip, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tip_like'


class TipCommentLike(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    tip_comment = models.ForeignKey(TipComment, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tcomment_like'
