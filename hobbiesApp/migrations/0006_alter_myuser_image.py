# Generated by Django 3.2.4 on 2021-12-10 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hobbiesApp', '0005_auto_20211204_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='image',
            field=models.ImageField(blank=True, default='default.png', null=True, upload_to=''),
        ),
    ]