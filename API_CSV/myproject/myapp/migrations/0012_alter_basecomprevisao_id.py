# Generated by Django 4.2.7 on 2023-12-05 02:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_alter_basecomprevisao_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basecomprevisao',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
