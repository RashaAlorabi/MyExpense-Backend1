

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='parent_image')),
                ('wallet', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1)])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('school_admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('grade', models.CharField(choices=[('Grade 1', 'Grade 1'), ('Grade 2', 'Grade 2'), ('Grade 3', 'Grade 3'), ('Grade 4', 'Grade 4'), ('Grade 5', 'Grade 5'), ('Grade 6', 'Grade 6')], default=1, max_length=10)),
                ('limit', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('image', models.ImageField(blank=True, null=True, upload_to='student_image')),
                ('health', models.CharField(max_length=50)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child', to='api.Parent')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='api.School')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('paid', models.BooleanField(default=False)),
                ('order_date', models.DateTimeField(null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='api.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('stock', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1)])),
                ('image', models.ImageField(blank=True, null=True, upload_to='item_image')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='api.Category')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='api.School')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schoolcategories', to='api.School'),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1)])),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Item')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='api.Order')),
            ],
        ),
    ]
