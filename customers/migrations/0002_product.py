# Generated by Django 5.2 on 2025-05-28 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to='product_images/')),
            ],
        ),
    ]
