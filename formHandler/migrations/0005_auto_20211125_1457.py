# Generated by Django 3.2.3 on 2021-11-25 12:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('formHandler', '0004_rename_nofirytelegram_formmodel_notifytelegram'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='emailnotify',
            unique_together={('email', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='telegramnotify',
            unique_together={('chat_id', 'name')},
        ),
    ]