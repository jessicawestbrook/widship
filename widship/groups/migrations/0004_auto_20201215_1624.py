# Generated by Django 3.1.4 on 2020-12-15 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0003_auto_20201215_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='create_datetime',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
