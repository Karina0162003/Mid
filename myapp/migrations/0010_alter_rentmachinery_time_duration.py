# Generated by Django 4.1.5 on 2024-02-01 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_alter_rentmachinery_rent_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentmachinery',
            name='time_duration',
            field=models.CharField(choices=[('1', '8:00 AM to 10:00 AM'), ('2', '10:00 AM to 12:00 PM'), ('3', '12:00 PM to 2:00 PM'), ('4', '2:00 PM to 4:00 PM'), ('5', '4:00 PM to 6:00 PM'), ('6', '6:00 PM TO 8:00 PM')], max_length=30),
        ),
    ]
