
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Voting',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('desc', models.TextField(blank=True, null=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('tally', models.Field(blank=True, default=[], null=True)),
                ('postproc', models.Field(blank=True, default=[], null=True)),
                ('auths', models.ManyToManyField(related_name='votings', to='base.Auth')),
                ('pub_key', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='voting', to='base.Key')),
                ('question', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, related_name='voting', to='voting.Question')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(blank=True, null=True)),
                ('option', models.TextField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='voting.Question')),
            ],
        ),
    ]
