# Generated by Django 2.2.10 on 2021-07-15 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0010_auto_20210715_1632'),
    ]

    operations = [
        migrations.CreateModel(
            name='condition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='question_element',
            name='is_random',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='question_element',
            name='conditions',
            field=models.ManyToManyField(null=True, to='application.condition'),
        ),
    ]
