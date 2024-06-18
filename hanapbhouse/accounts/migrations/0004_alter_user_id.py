# Generated by Django 5.0.6 on 2024-06-09 09:12

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='id',
            field=models.CharField(default=accounts.models.generate_custom_id, editable=False, max_length=17, primary_key=True, serialize=False, unique=True),
        ),
    ]
