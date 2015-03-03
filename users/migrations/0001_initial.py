# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default=b'P', max_length=1, choices=[(b'P', b'pending'), (b'A', b'accepted'), (b'R', b'rejected')])),
                ('receiver', models.ForeignKey(related_name='friendships_by_receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(related_name='friendships_by_sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='friendship',
            unique_together=set([('sender', 'receiver')]),
        ),
    ]
