# Generated by Django 4.2 on 2024-08-08 10:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('chain_id', models.IntegerField()),
                ('start_block', models.BigIntegerField()),
                ('last_scanned_block', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Symbol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, unique=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BalanceModifier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_address', models.CharField(max_length=42)),
                ('function_signature', models.CharField(max_length=255)),
                ('params_mask', models.JSONField()),
                ('receiver', models.IntegerField()),
                ('value', models.IntegerField()),
                ('value_amount', models.BigIntegerField(default=0)),
                ('chain', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='symbol.chain')),
                ('symbol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modifiers', to='symbol.symbol')),
            ],
        ),
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.BigIntegerField(default=0)),
                ('symbol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='symbol.symbol')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
