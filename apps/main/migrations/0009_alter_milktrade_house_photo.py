# Generated by Django 4.2.3 on 2023-07-29 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_milktrade_delete_producer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='milktrade',
            name='house_photo',
            field=models.ImageField(default='', upload_to='uploads/'),
            preserve_default=False,
        ),
    ]
