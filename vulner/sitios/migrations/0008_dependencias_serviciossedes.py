# Generated by Django 3.2 on 2022-02-05 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sitios', '0007_auto_20220205_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='dependencias',
            name='serviciosSedes',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='serviciosSedes1', to='sitios.serviciossedes'),
        ),
    ]