# Generated by Django 5.0.3 on 2024-04-05 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sidebar', '0003_alter_notification_notification_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='title',
            field=models.CharField(default='New task', max_length=100),
        ),
    ]
