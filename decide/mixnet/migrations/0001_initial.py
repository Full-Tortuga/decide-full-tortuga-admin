<<<<<<< HEAD
# Generated by Django 2.2.5 on 2021-12-11 12:30
=======
# Generated by Django 2.2.5 on 2021-12-11 16:57
>>>>>>> f2ac03dae091252e300b9391543f807a3599f798

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mixnet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voting_id', models.PositiveIntegerField()),
                ('auth_position', models.PositiveIntegerField(default=0)),
                ('auths', models.ManyToManyField(related_name='mixnets', to='base.Auth')),
                ('key', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mixnets', to='base.Key')),
                ('pubkey', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mixnets_pub', to='base.Key')),
            ],
        ),
    ]
