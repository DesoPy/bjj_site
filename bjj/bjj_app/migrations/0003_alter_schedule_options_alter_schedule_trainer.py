# Generated by Django 4.2 on 2023-05-20 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bjj_app', '0002_trainer_schedule'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='schedule',
            options={'verbose_name': 'Schedule'},
        ),
        migrations.AlterField(
            model_name='schedule',
            name='trainer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bjj_app.trainer'),
        ),
    ]