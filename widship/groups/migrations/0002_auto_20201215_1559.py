# Generated by Django 3.1.4 on 2020-12-15 20:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='creator',
            new_name='creator_username',
        ),
    ]
