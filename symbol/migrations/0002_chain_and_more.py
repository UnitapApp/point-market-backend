# Generated by Django 4.2 on 2024-08-03 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('symbol', '0001_initial'),
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
        migrations.RenameField(
            model_name='balancemodifier',
            old_name='function_name',
            new_name='function_signature',
        ),
        migrations.AlterField(
            model_name='balancemodifier',
            name='symbol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modifiers', to='symbol.symbol'),
        ),
        migrations.AddField(
            model_name='balancemodifier',
            name='chain',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='symbol.chain'),
            preserve_default=False,
        ),
    ]
