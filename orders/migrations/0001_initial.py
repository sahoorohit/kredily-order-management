# Generated by Django 4.0.4 on 2022-04-20 08:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('amount', models.IntegerField(default=0)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('item_name', models.CharField(max_length=256)),
                ('unit_price', models.IntegerField(default=0)),
                ('quantity', models.IntegerField(default=0)),
                ('amount', models.IntegerField(default=0)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='suborders', to='orders.order')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
