# Generated by Django 2.2.12 on 2021-08-20 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supermarket', '0007_auto_20210820_0833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='total_birr',
            field=models.FloatField(default=56789),
        ),
    ]
