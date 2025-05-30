# Generated by Django 5.1.6 on 2025-03-06 12:00

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('json_app', '0008_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='IngestProd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(default=None, max_length=255)),
                ('ingestion_id', models.CharField(max_length=255, unique=True)),
                ('ingestion_item_id', models.CharField(blank=True, max_length=255, null=True)),
                ('batch_id', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(default='Pending', max_length=50)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'ingestprod',
            },
        ),
        migrations.AlterField(
            model_name='ingestionlog',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='jsonfile',
            name='batch_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='sourcemetadata',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
