# Generated by Django 4.1.5 on 2023-02-04 01:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0002_vehicle_order_drivertovehicle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='driver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='driver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='order',
            name='sharer',
            field=models.ManyToManyField(blank=True, null=True, related_name='sharer', to=settings.AUTH_USER_MODEL),
        ),
    ]