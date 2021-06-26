from django.contrib import admin
from .models import IPL
import csv
#Register your models here.
def run():
    fhand = open('matches.csv')
    reader = csv.reader(fhand)
    i = 0
    IPL.objects.all().delete()

    for row in reader:
        #id,city,date,player_of_match,venue,neutral_venue,team1,team2,toss_winner,toss_decision,winner,result,result_margin,eliminator,method,umpire1,umpire2
        print(row)
        #id,season,city,date,team1,team2,toss_winner,toss_decision,result,dl_applied,winner,win_by_runs,win_by_wickets,player_of_match,venue,umpire1,umpire2,umpire3
        IPL.objects.get_or_create(season=row[1],city=row[2],date=row[3],team1=row[4],team2=row[5],toss_winner=row[6],toss_decision=row[7],result=row[8],dl_applied=row[9],winner=row[10],win_by_runs=row[11],win_by_wickets=row[12],player_of_match=row[13],venue=row[14],umpire1=row[15],umpire2=row[16],umpire3=row[17])
run()
admin.site.register(IPL)