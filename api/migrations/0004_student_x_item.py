# Generated by Django 2.2 on 2019-04-24 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20190421_1328'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='x_item',
            field=models.ManyToManyField(blank=True, null=True, related_name='x_items', to='api.Item'),
        ),
    ]
