# Generated by Django 2.2 on 2019-04-26 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20190426_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='grade',
            field=models.CharField(choices=[('الصف الاول', 'الصف الاول'), ('الصف الثاني', 'الصف الثاني'), ('الصف الثالث', 'الصف الثالث'), ('الصف الرابع', 'الصف الرابع'), ('الصف الخامس', 'الصف الخامس'), ('الصف السادس', 'الصف السادس')], default=1, max_length=20),
        ),
    ]
