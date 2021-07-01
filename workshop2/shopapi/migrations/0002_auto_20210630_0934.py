# Generated by Django 3.2.4 on 2021-06-30 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name_plural': 'Cart'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Category'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name_plural': 'Product'},
        ),
        migrations.AlterModelOptions(
            name='product_image',
            options={'verbose_name_plural': 'Product Image'},
        ),
        migrations.AlterField(
            model_name='product_image',
            name='img_product',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='shopapi.product'),
        ),
    ]
