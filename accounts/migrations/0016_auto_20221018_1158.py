# Generated by Django 3.2.15 on 2022-10-18 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_creator_last_logout'),
    ]

    operations = [
        migrations.AddField(
            model_name='admins',
            name='last_logout',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='last_logout',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
