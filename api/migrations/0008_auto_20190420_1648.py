# Generated by Django 2.2 on 2019-04-20 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_school_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='school',
            name='category',
        ),
        migrations.AddField(
            model_name='category',
            name='school',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='schoolitems', to='api.School'),
            preserve_default=False,
        ),
    ]
