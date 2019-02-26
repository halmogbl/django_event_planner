# Generated by Django 2.1 on 2019-02-25 22:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_ticket_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='tickets',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='event',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='events.Event'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]