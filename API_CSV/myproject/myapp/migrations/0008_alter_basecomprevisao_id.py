# Generated by Django 4.2.7 on 2023-12-05 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_basecomprevisao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basecomprevisao',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]