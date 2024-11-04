# Generated by Django 5.1.2 on 2024-11-04 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursemember',
            name='roles',
            field=models.CharField(choices=[('std', 'Siswa'), ('ast', 'Asisten')], default='std', max_length=50, verbose_name='peran'),
        ),
    ]