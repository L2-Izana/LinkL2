# Generated by Django 5.0.3 on 2024-04-04 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sidebar', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
