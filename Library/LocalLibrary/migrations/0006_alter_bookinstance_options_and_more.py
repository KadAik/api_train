# Generated by Django 5.1.5 on 2025-02-11 14:11

import django.db.models.functions.text
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LocalLibrary', '0005_bookinstance_borrower'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned', 'Set book as returned'),)},
        ),
        migrations.RemoveConstraint(
            model_name='genre',
            name='genre_name_case_insensitive_unqie',
        ),
        migrations.AddConstraint(
            model_name='genre',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('name'), name='genre_name_case_insensitive_unique', violation_error_message='Genre already exists (case insensitive match)'),
        ),
    ]
