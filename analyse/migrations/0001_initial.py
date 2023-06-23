# Generated by Django 4.2 on 2023-06-04 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DatasetFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_title', models.CharField(max_length=250)),
                ('file_field', models.FileField(unique=True, upload_to='datasets/')),
                ('added_dt', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'unique_together': {('file_title', 'file_field', 'added_dt')},
            },
        ),
    ]
