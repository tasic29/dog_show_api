# Generated by Django 5.0.2 on 2024-03-02 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exibition', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='judge',
            options={'ordering': ['id']},
        ),
        migrations.RemoveField(
            model_name='owner',
            name='address',
        ),
        migrations.RemoveField(
            model_name='owner',
            name='phone',
        ),
    ]
