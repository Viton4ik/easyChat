# Generated by Django 4.1.7 on 2023-03-15 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_alter_message_chat_alter_message_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ('createTime',)},
        ),
    ]
