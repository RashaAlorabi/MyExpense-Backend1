# Generated by Django 2.2 on 2019-04-19 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20190419_0701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='grade',
            field=models.IntegerField(choices=[('Grade1', 'Grade1'), ('Grade2', 'Grade2'), ('Grade3', 'Grade3'), ('Grade4', 'Grade4'), ('Grade5', 'Grade5'), ('Grade6', 'Grade6')], default=1),
        ),
    ]