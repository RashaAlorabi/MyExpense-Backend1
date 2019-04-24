# Generated by Django 2.2 on 2019-04-24 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_student_x_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='x_item',
        ),
        migrations.AddField(
            model_name='student',
            name='not_allowed',
            field=models.ManyToManyField(related_name='not_alloweds', to='api.Item'),
        ),
    ]
