# Generated by Django 2.2.7 on 2021-06-26 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IPL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season', models.IntegerField(default=0, verbose_name='season')),
                ('city', models.CharField(default='NA', max_length=255, verbose_name='city')),
                ('date', models.DateField(verbose_name='date')),
                ('team1', models.CharField(default='NA t1', max_length=255, verbose_name='team1')),
                ('team2', models.CharField(default='NA t2', max_length=255, verbose_name='team2')),
                ('toss_winner', models.CharField(default='NA tw', max_length=248, verbose_name='toss_winner')),
                ('toss_decision', models.CharField(default='NA td', max_length=247, verbose_name='toss_decision')),
                ('result', models.CharField(default='NA res', max_length=245, verbose_name='result')),
                ('dl_applied', models.CharField(default='NA', max_length=245, verbose_name='dl_applied')),
                ('winner', models.CharField(default='NA w', max_length=246, verbose_name='winner')),
                ('win_by_runs', models.IntegerField(default=0, verbose_name='win_by_runs')),
                ('win_by_wickets', models.IntegerField(default=0, verbose_name='win_by_wickets')),
                ('player_of_match', models.CharField(default='NA pom', max_length=254, verbose_name='player_of_match')),
                ('venue', models.CharField(default='NA ven', max_length=253, verbose_name='venue')),
                ('umpire1', models.CharField(default='NA ump1', max_length=242, verbose_name='umpire1')),
                ('umpire2', models.CharField(default='NA ump2', max_length=241, verbose_name='umpire2')),
                ('umpire3', models.CharField(default='NA ump2', max_length=241, verbose_name='umpire2')),
            ],
            options={
                'verbose_name_plural': 'IPL',
            },
        ),
    ]
