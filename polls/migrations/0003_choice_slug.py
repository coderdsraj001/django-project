# Generated by Django 3.2.20 on 2023-08-23 08:55

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_question_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='slug',
            field=autoslug.fields.AutoSlugField(default=None, editable=False, null=True, populate_from='choice_text', unique=True),
        ),
    ]
