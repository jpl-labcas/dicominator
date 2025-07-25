# Generated by Django 4.2.23 on 2025-07-09 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jpllabcasdicominatortags", "0003_alter_series_software_versions"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="dicomtag",
            name="tag",
        ),
        migrations.RemoveField(
            model_name="dicomtag",
            name="uid",
        ),
        migrations.AlterField(
            model_name="dicomtag",
            name="level",
            field=models.IntegerField(
                choices=[(1, "STUDY"), (2, "SERIES"), (3, "IMAGE")]
            ),
        ),
    ]
