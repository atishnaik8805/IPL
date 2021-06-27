# from django.db import models


# # Create your models here.
# class Search(models.Model):
#     search = models.CharField(max_length=500)
#     created = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name_plural = 'Searches'

#     def __str__(self):
#         return '{}'.format(self.search)
from datetime import datetime, timezone
from django.db import models
from django.utils.translation import gettext as _

# Create your models here. id,city,date,player_of_match,venue,neutral_venue,team1,team2,toss_winner,toss_decision,winner,result,result_margin,eliminator,method,umpire1,umpire2
class IPL(models.Model):
    id = models.AutoField(_('id'), auto_created=False, primary_key=True, serialize=False, unique=True)
    #id,season,city,date,team1,team2,toss_winner,toss_decision,result,dl_applied,winner,win_by_runs,win_by_wickets,player_of_match,venue,umpire1,umpire2,umpire3
    season =  models.IntegerField(_('season'), default=0)
    city = models.CharField(_('city'), default='NA', max_length=255)
    date = models.DateField(_('date'),auto_now=False)
    team1 = models.CharField(_('team1'), default='NA t1', max_length=255)
    team2 = models.CharField(_('team2'), default='NA t2', max_length=255)
    toss_winner = models.CharField(_('toss_winner'), default='NA tw', max_length=248)
    toss_decision = models.CharField(_('toss_decision'), default='NA td',max_length=247)
    result = models.CharField(_('result'), default='NA res', max_length=245)
    dl_applied = models.CharField(_('dl_applied'), default='NA', max_length=245)
    winner = models.CharField(_('winner'), default='NA w', max_length=246)
    win_by_runs = models.IntegerField(_('win_by_runs'), default=0)
    win_by_wickets = models.IntegerField(_('win_by_wickets'), default=0)
    player_of_match = models.CharField(_('player_of_match'), default='NA pom', max_length=254)
    venue = models.CharField(_('venue'), default='NA ven', max_length=253)
    umpire1 = models.CharField(_('umpire1'), default='NA ump1', max_length=242)
    umpire2 = models.CharField(_('umpire2'), default='NA ump2', max_length=241)
    umpire3 = models.CharField(_('umpire2'), default='NA ump2', max_length=241)

    #field_order = ['id','city','date','player_of_match','venue','neutral_venue','team1','team2','toss_winner','toss_decision','winner','result','result_margin','eliminator','method','umpire1','umpire2']

    class Meta:
        verbose_name_plural = 'IPL'

    def __str__(self):
        return self
