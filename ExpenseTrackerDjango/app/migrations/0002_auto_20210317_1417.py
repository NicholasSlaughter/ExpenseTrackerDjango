# Generated by Django 2.1.15 on 2021-03-17 21:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alert',
            name='application_user',
        ),
        migrations.RemoveField(
            model_name='expense',
            name='application_user',
        ),
        migrations.DeleteModel(
            name='ApplicationUser',
        ),
    ]