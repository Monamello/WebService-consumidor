# Generated by Django 2.1.3 on 2018-11-26 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consumer', '0005_individuo_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individuo',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
