# Generated by Django 4.0.3 on 2022-05-09 18:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_complains'),
    ]

    operations = [
        migrations.RenameField(
            model_name='complains',
            old_name='lodgerid',
            new_name='lodger',
        ),
        migrations.RenameField(
            model_name='complains',
            old_name='Perpenetrers',
            new_name='perpenetrer',
        ),
    ]
