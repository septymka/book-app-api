# Generated by Django 4.1.2 on 2022-11-22 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_alter_book_image_alter_book_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='rating',
            field=models.FloatField(blank=True, null=True),
        ),
    ]