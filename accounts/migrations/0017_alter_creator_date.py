# Generated by Django 3.2.15 on 2022-10-31 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20221018_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creator',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
