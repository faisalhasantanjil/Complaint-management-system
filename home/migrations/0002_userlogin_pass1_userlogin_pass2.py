# Generated by Django 4.0.3 on 2022-04-13 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlogin',
            name='pass1',
            field=models.CharField(default='pass', max_length=50),
        ),
        migrations.AddField(
            model_name='userlogin',
            name='pass2',
            field=models.CharField(default='pass', max_length=50),
        ),
    ]
