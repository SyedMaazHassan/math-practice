# Generated by Django 2.2.10 on 2021-07-16 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0016_auto_20210716_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='image',
            field=models.ImageField(null=True, upload_to='media/exercise_icon'),
        ),
    ]
