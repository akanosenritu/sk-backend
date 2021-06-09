# Generated by Django 3.2.3 on 2021-06-09 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_mail_sender'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailsforevent',
            name='confirm_date_limit',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='mail',
            name='recipient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mail', to='api.registeredstaff'),
        ),
        migrations.AlterField(
            model_name='mailsforevent',
            name='mails',
            field=models.ManyToManyField(related_name='event', to='api.Mail'),
        ),
    ]