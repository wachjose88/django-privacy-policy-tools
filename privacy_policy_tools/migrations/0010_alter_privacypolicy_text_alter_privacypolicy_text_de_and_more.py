# Generated by Django 4.2.3 on 2024-03-12 15:39

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('privacy_policy_tools', '0009_onetimetoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privacypolicy',
            name='text',
            field=tinymce.models.HTMLField(verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='privacypolicy',
            name='text_de',
            field=tinymce.models.HTMLField(null=True, verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='privacypolicy',
            name='text_en',
            field=tinymce.models.HTMLField(null=True, verbose_name='Text'),
        ),
    ]
