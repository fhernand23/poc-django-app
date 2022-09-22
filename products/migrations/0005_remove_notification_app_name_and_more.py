# Generated by Django 4.0.7 on 2022-09-19 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_archived_provider_archived'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='app_name',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='dest_user_id',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='file_resource',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='id_file',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='tags',
        ),
        migrations.AddField(
            model_name='notification',
            name='attach',
            field=models.FileField(blank=True, null=True, upload_to='files/notifications'),
        ),
        migrations.AddField(
            model_name='notification',
            name='from_user_id',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='title',
            field=models.CharField(default='Notification title', max_length=120),
        ),
        migrations.AlterField(
            model_name='notification',
            name='content',
            field=models.TextField(default='Notification content'),
        ),
    ]