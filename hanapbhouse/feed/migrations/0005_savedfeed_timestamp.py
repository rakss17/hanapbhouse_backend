# Generated by Django 5.0.6 on 2024-06-14 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0004_alter_savedfeed_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='savedfeed',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
