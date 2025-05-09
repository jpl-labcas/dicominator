# Generated by Django 4.2.21 on 2025-05-09 16:08

from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailcore", "0089_log_entry_data_json_null_to_object"),
    ]

    operations = [
        migrations.CreateModel(
            name="FlexPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "body",
                    wagtail.fields.StreamField(
                        [
                            (
                                "rich_text",
                                wagtail.blocks.RichTextBlock(
                                    help_text="Richly formatted text",
                                    icon="doc-full",
                                    label="Rich Text",
                                ),
                            ),
                            (
                                "raw_html",
                                wagtail.blocks.RawHTMLBlock(
                                    help_text="Raw HTML (use with care)"
                                ),
                            ),
                        ],
                        blank=True,
                        null=True,
                        use_json_field=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "web page",
                "verbose_name_plural": "web pages",
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="HomePage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "body",
                    wagtail.fields.StreamField(
                        [
                            (
                                "rich_text",
                                wagtail.blocks.RichTextBlock(
                                    help_text="Richly formatted text",
                                    icon="doc-full",
                                    label="Rich Text",
                                ),
                            ),
                            (
                                "raw_html",
                                wagtail.blocks.RawHTMLBlock(
                                    help_text="Raw HTML (use with care)"
                                ),
                            ),
                        ],
                        blank=True,
                        null=True,
                        use_json_field=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "home page",
                "verbose_name_plural": "home pages",
            },
            bases=("wagtailcore.page",),
        ),
    ]
