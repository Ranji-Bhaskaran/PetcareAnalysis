""" Initial migration """
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """ Migration class """
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=200)),
                ('message', models.TextField(
                    validators=[django.core.validators.MaxLengthValidator(1000)])),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(
                    default='product_images/default.jpeg', upload_to='product_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('breed', models.CharField(max_length=100)),
                ('age', models.PositiveIntegerField(
                    help_text='Age of pet in years.')),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('image', models.ImageField(
                    blank=True, null=True, upload_to='pet_images/')),
                ('owner', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HealthLog',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_date', models.DateField()),
                ('weight', models.FloatField()),
                ('rabies', models.CharField(
                    choices=[('yes', 'Yes'), ('no', 'No')], default='no', max_length=3)),
                ('deworming', models.CharField(
                    choices=[('yes', 'Yes'), ('no', 'No')], default='no', max_length=3)),
                ('pet', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='pets.pet')),
            ],
        ),
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_date', models.DateField()),
                ('activity_type', models.CharField(
                    choices=[
                        ('walk', 'Walk'),('play', 'Play'),('groom', 'Grooming')], max_length=100)),
                ('duration', models.PositiveIntegerField(help_text='Duration in minutes.')),
                ('pet', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='pets.pet')),
            ],
        ),
    ]
