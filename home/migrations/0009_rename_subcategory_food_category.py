# Generated by Django 4.2.3 on 2024-07-27 06:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_food_tags_alter_food_subcategory_delete_subcategory'),
    ]

    operations = [
        migrations.RenameField(
            model_name='food',
            old_name='subcategory',
            new_name='category',
        ),
    ]
