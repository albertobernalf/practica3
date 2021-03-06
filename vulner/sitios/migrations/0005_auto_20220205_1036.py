# Generated by Django 3.2 on 2022-02-05 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinico', '0002_initial'),
        ('sitios', '0004_serviciossedes_constraint_serviciossedes'),
    ]

    operations = [
        migrations.AddField(
            model_name='dependencias',
            name='sedesClinica',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.PROTECT, to='sitios.sedesclinica'),
        ),
        migrations.AddField(
            model_name='dependencias',
            name='servicios',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.PROTECT, to='clinico.servicios'),
        ),
    ]
