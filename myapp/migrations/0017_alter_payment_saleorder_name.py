# Generated by Django 4.1.5 on 2024-03-04 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_remove_customer_area_name_remove_customer_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='saleorder_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.salesorder_detail'),
        ),
    ]
