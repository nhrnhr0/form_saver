# Generated by Django 3.2.3 on 2021-05-31 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formHandler', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='formmodel',
            name='successRedirect',
            field=models.URLField(default='/success'),
        ),
    ]
