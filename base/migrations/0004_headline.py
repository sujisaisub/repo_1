# Generated by Django 3.0.6 on 2020-07-11 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_feedback_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='Headline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', models.URLField(blank=True, null=True)),
                ('url', models.TextField()),
            ],
        ),
    ]
