# Generated by Django 3.2 on 2022-02-05 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitios', '0006_auto_20220205_1042'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='dependencias',
            name='Constraint_dependencias',
        ),
        migrations.AddConstraint(
            model_name='dependencias',
            constraint=models.UniqueConstraint(fields=('sedesClinica', 'servicios', 'dependenciasTipo', 'numero'), name='Constraint_dependencias'),
        ),
    ]
