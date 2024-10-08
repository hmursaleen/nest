# Generated by Django 5.1 on 2024-09-04 09:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blogs', '0001_initial'),
        ('comments', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Buzz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comments.comment')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogs.blogpost')),
                ('trigger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='triggered_buzzes', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buzzes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Buzz',
                'verbose_name_plural': 'Buzzes',
                'ordering': ['-created_at'],
            },
        ),
    ]
