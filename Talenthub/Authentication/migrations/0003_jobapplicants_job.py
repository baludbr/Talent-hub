# Generated by Django 4.2.5 on 2024-02-02 05:04

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Authentication", "0002_alter_candidates_us_id_alter_user_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="JobApplicants",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("job_id", models.BigIntegerField(null=True)),
                ("candidate_id", models.TextField(null=True)),
                ("status", models.CharField(blank=True, max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name="Job",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("company", models.CharField(max_length=255)),
                ("location", models.CharField(max_length=255)),
                (
                    "salary",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("published_at", models.DateTimeField(auto_now_add=True)),
                (
                    "application_deadline",
                    models.DateField(blank=True, default=datetime.datetime.today),
                ),
                ("application_status", models.BooleanField(default=True)),
                (
                    "posted_by",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Authentication.user",
                    ),
                ),
            ],
        ),
    ]