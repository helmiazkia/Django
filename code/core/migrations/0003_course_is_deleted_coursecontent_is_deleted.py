# Generated by Django 5.1.2 on 2024-11-04 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_coursemember_roles'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='coursecontent',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
