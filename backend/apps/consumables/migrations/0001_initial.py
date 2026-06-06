from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ConsumableCategory",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True)),
                ("unit", models.CharField(default="pcs", max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="Consumable",
            fields=[
                ("id", models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ("brand", models.CharField(blank=True, max_length=100)),
                ("model_number", models.CharField(blank=True, max_length=100)),
                ("unit", models.CharField(default="pcs", max_length=20)),
                ("price", models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ("supplier", models.URLField(blank=True, max_length=500)),
                ("purchase_url", models.URLField(blank=True, max_length=500)),
                ("notes", models.TextField(blank=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("category", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="consumables", to="consumables.consumablecategory")),
                ("family", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="consumables", to="accounts.family")),
                ("owner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="consumables", to="accounts.user")),
            ],
        ),
        migrations.CreateModel(
            name="ConsumableStock",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("quantity", models.DecimalField(decimal_places=2, max_digits=10)),
                ("location", models.CharField(blank=True, max_length=200)),
                ("expiry_date", models.DateField(null=True)),
                ("recorded_at", models.DateTimeField(auto_now_add=True)),
                ("consumable", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="stock_records", to="consumables.consumable")),
            ],
        ),
    ]
