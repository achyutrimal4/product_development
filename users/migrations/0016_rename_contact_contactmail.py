# Generated by Django 4.1 on 2022-09-19 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_alter_contact_options_remove_contact_msg_title_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Contact',
            new_name='ContactMail',
        ),
    ]
