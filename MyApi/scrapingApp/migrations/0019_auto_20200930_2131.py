# Generated by Django 3.1.1 on 2020-09-30 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapingApp', '0018_theodoteam'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TheodoTeam',
        ),
        migrations.AddField(
            model_name='parliament1',
            name='dob',
            field=models.TextField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='parliament1',
            name='pp',
            field=models.TextField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='parliament1',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
