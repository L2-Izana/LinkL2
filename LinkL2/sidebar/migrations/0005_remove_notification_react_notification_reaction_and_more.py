# Generated by Django 5.0.3 on 2024-04-05 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sidebar', '0004_task_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='react',
        ),
        migrations.AddField(
            model_name='notification',
            name='reaction',
            field=models.CharField(blank=True, choices=[('Like', 'Like'), ('Love', 'Love'), ('Haha', 'Haha'), ('Wow', 'Wow'), ('Sad', 'Sad'), ('Angry', 'Angry')], max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
