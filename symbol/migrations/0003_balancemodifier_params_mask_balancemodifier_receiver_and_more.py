# Generated by Django 4.2 on 2024-08-05 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('symbol', '0002_chain_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='balancemodifier',
            name='params_mask',
            field=models.JSONField(default=[]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='balancemodifier',
            name='receiver',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='balancemodifier',
            name='value_amount',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='balancemodifier',
            name='value',
            field=models.IntegerField(),
        ),
    ]
