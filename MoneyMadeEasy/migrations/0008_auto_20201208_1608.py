# Generated by Django 3.1 on 2020-12-08 22:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MoneyMadeEasy', '0007_auto_20201205_1247'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='int_rate',
        ),
        migrations.RemoveField(
            model_name='expense',
            name='outstanding',
        ),
        migrations.RemoveField(
            model_name='expense',
            name='term_len',
        ),
    ]