# Generated by Django 5.1.7 on 2025-04-29 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study_companion', '0019_parceria'),
    ]

    operations = [
        migrations.AddField(
            model_name='parceria',
            name='aceita',
            field=models.BooleanField(default=False),
        ),
    ]
