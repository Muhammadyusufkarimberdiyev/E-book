# Generated by Django 5.1.1 on 2024-10-16 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_book_options_book_file_alter_book_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='dislikes',
        ),
        migrations.RemoveField(
            model_name='book',
            name='likes',
        ),
        migrations.AlterField(
            model_name='book',
            name='text',
            field=models.TextField(help_text='Kitob matnini yozing'),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=50, verbose_name='Kitob nomi'),
        ),
    ]
