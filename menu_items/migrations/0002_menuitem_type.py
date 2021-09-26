# Generated by Django 3.2.5 on 2021-08-28 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu_items', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='type',
            field=models.CharField(choices=[('appetizer', 'Appetizer'), ('main', 'Main'), ('dessert', 'Dessert'), ('drink', 'Drink')], default='main', max_length=10),
        ),
    ]