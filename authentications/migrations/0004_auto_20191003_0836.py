# Generated by Django 2.2.5 on 2019-10-03 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentications', '0003_auto_20191001_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='is active'),
        ),
    ]