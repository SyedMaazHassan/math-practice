# Generated by Django 2.2.10 on 2021-07-16 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0017_auto_20210716_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='exercise',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='application.exercise'),
        ),
        migrations.AddField(
            model_name='question',
            name='topic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='application.topic'),
        ),
    ]
