# Generated by Django 4.2.4 on 2023-08-11 12:05

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):
    dependencies = [
        ("user_module", "0005_alter_qualificationinfo_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="educationinfo",
            name="institution_name",
            field=models.CharField(max_length=100, verbose_name="School Name"),
        ),
    ]