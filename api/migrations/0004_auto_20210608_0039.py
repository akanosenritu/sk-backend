# Generated by Django 3.2.3 on 2021-06-07 15:39

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_application_mail_mailsforevent'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailTemplate',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('template', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='mailsforevent',
            name='associated_data',
        ),
        migrations.RemoveField(
            model_name='mailsforevent',
            name='template',
        ),
        migrations.AddField(
            model_name='mailsforevent',
            name='default_template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.mailtemplate'),
        ),
    ]
