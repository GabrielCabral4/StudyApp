# Generated by Django 5.1.7 on 2025-04-11 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study_companion', '0003_alter_disciplina_periodo'),
    ]

    operations = [
        migrations.AddField(
            model_name='disciplina',
            name='cor_hex',
            field=models.CharField(default='#FFFFFF', max_length=7),
        ),
    ]
