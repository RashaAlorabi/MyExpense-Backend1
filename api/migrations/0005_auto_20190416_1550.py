# Generated by Django 2.2 on 2019-04-16 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20190416_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parent',
            name='school',
            field=models.ManyToManyField(related_name='parents', to='api.School'),
        ),
    ]
