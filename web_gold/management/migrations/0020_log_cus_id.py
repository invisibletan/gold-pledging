# Generated by Django 3.0.4 on 2020-04-25 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0019_auto_20200425_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='cus_id',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='management.Customer'),
            preserve_default=False,
        ),
    ]
