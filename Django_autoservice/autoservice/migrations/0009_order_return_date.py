# Generated by Django 5.1.3 on 2024-12-05 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoservice', '0008_rename_reader_order_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='return_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]