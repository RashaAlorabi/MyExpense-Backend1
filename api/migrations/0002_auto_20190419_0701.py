# Generated by Django 2.2 on 2019-04-19 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='grade',
            field=models.IntegerField(choices=[('Grade1', 'Grade 1'), ('Grade2', 'Grade 2'), ('Grade3', 'Grade 3'), ('Grade4', 'Grade 4'), ('Grade5', 'Grade 5'), ('Grade6', 'Grade 6')], default=1),
        ),
    ]
