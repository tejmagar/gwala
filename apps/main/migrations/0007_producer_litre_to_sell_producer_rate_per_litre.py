# Generated by Django 4.2.3 on 2023-07-26 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_producer_milk_source_delete_milksource'),
    ]

    operations = [
        migrations.AddField(
            model_name='producer',
            name='litre_to_sell',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='producer',
            name='rate_per_litre',
            field=models.IntegerField(default=1, help_text='In rupees'),
            preserve_default=False,
        ),
    ]
