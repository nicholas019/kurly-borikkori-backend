# Generated by Django 4.1 on 2022-08-21 04:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='main_category',
        ),
        migrations.AddField(
            model_name='subcategory',
            name='main_category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='recipes.maincategory'),
            preserve_default=False,
        ),
    ]
