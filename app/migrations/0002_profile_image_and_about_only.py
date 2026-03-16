# Generated manually for Profile: keep only hero_image and about_text

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(model_name='profile', name='name'),
        migrations.RemoveField(model_name='profile', name='professional_title'),
        migrations.RemoveField(model_name='profile', name='created_at'),
        migrations.RemoveField(model_name='profile', name='updated_at'),
    ]
