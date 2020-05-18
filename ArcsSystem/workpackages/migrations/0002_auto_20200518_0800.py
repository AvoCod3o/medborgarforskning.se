# Generated by Django 2.2.12 on 2020-05-18 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workpackages', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='theme',
            options={'verbose_name': 'Theme', 'verbose_name_plural': 'Themes'},
        ),
        migrations.AlterModelOptions(
            name='workpackage',
            options={'verbose_name': 'Work package', 'verbose_name_plural': 'Work packages'},
        ),
        migrations.AddField(
            model_name='workpackage',
            name='detailed_content_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='workpackage',
            name='detailed_content_sv',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='workpackage',
            name='introduction_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='workpackage',
            name='introduction_sv',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='workpackage',
            name='name_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='workpackage',
            name='name_sv',
            field=models.TextField(null=True),
        ),
    ]
