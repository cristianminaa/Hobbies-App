# Generated by Django 3.2.7 on 2021-12-04 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hobbiesApp', '0002_alter_myuser_hobbies'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='name',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
