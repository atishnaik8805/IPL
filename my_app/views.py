from collections import Counter
from os import environ
import os
from django.db.models.aggregates import Count, Max, Min
from django.db.models.expressions import F
import pymongo
import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from . import models


# Create your views here.
def home(request):
    dates = models.IPL.objects.values().dates('date', 'year')
    setYears ={
      'years': list(dates)
    }
    return render(request, 'base.html', setYears)


def yeardata(request):
    class returnList:
        @property
        def returnItems(self):
            return enumerate(self.items())
    year = request.POST.get('year')
    dates = models.IPL.objects.values().dates('date', 'year')
    #print('Yo', year)
    #q1
    top4=dict()
    qs = models.IPL.objects.values('team1', 'team2', 'winner').filter(date__year=year).order_by('-id')[:20]
    top4qs = qs[:4]
    #1
    one = top4qs[0]['winner']
    top4['1'] = one
    #2
    two = ''
    if top4qs[0]['team1'] == one:
        two = top4qs[0]['team2']
        top4['2'] = two
    else:
        two = top4qs[0]['team1']
        top4['2'] = two
    #3
    three = ''
    if top4qs[1]['winner'] != top4qs[1]['team1']:
        three = top4qs[1]['team1']
        top4['3'] = three
    else:
        three = top4qs[1]['team2']
        top4['3'] = three
    #4
    four = ''
    if top4qs[2]['winner'] != top4qs[2]['team1']:
        four = top4qs[2]['team1']
        top4['4'] = four
    else:
        four = top4qs[2]['team2']
        top4['4'] = four
    
    #print(top4)
    

    #print(top4qs)

    #q2
    tossWins = models.IPL.objects.values('toss_winner').annotate(countoftosswins= Count('toss_winner')).filter(date__year=year)
    maxValue = tossWins.aggregate(Max('countoftosswins'))['countoftosswins__max']
    maxTossWinsTeam = {}
    #print(tossWins.aggregate(Max('countoftosswins')))
    #print(tossWins.aggregate(Max('countoftosswins'))['countoftosswins__max'])
    for obj in tossWins:
        if obj['countoftosswins'] == maxValue:
            maxTossWinsTeam = obj
    #print('maxToss', maxTossWinsTeam)
    
    
    #q3
    pomWins = models.IPL.objects.values('player_of_match').annotate(countofpomwins= Count('player_of_match')).filter(date__year=year)
    maxValue = pomWins.aggregate(Max('countofpomwins'))['countofpomwins__max']
    maxPomWinsTeam = {}
    for obj in pomWins:
        if obj['countofpomwins'] == maxValue:
            maxPomWinsTeam = obj
    
    #print('maxPOM', maxPomWinsTeam)

    #q4
    teamWins = models.IPL.objects.values('winner').annotate(countofteamwins= Count('winner')).filter(date__year=year)
    maxValue = teamWins.aggregate(Max('countofteamwins'))['countofteamwins__max']
    maxteamWinsTeam = {}
    for obj in teamWins:
        if obj['countofteamwins'] == maxValue:
            maxteamWinsTeam = obj
    
    #print('maxTemsWins' , maxteamWinsTeam)

    #q5
    venueWins = models.IPL.objects.values('venue').annotate(countofvenuewins= Count('venue')).filter(date__year=year, winner=one)
    maxValue = venueWins.aggregate(Max('countofvenuewins'))['countofvenuewins__max']
    maxVenueWins = {}
    for obj in venueWins:
        if obj['countofvenuewins'] == maxValue:
            maxVenueWins = obj
    
    #print('max Venue', maxVenueWins)
    #q6
    totalCount = models.IPL.objects.filter(date__year=year).count()
    percBatQs = models.IPL.objects.filter(date__year=year, toss_decision = 'bat').aggregate(bats = Count('id'))
    # print(percBatQs['bats'] * 100 / totalCount)
    # print(percBatQs['bats'])
    # print(totalCount)

    #print('%', percBatQs)

    #q7
    venue = models.IPL.objects.values('venue').annotate(countofvenue= Count('venue')).filter(date__year=year)
    maxValue = venue.aggregate(Max('countofvenue'))['countofvenue__max']
    maxVenue = {}
    for obj in venue:
        if obj['countofvenue'] == maxValue:
            maxVenue = obj
    
    #print('max Venue', maxVenue)

    #q8
    runMargins = models.IPL.objects.values('win_by_runs', 'team1', 'team2', 'winner', 'venue').filter(date__year=year, win_by_runs__gt = 0)
    #print(runMargins)
    #print(runMargins.aggregate(Max('win_by_runs')))
    maxValue = runMargins.aggregate(Max('win_by_runs'))['win_by_runs__max']
    maxRunMargin = {}
    for obj in runMargins:
        if obj['win_by_runs'] == maxValue:
            maxRunMargin = obj
    
    #print('maXMArhin', maxRunMargin)
    
    #q2.1
    wicketsMargins = models.IPL.objects.values('win_by_wickets', 'team1', 'team2', 'winner', 'venue').filter(date__year=year, win_by_wickets__gt = 0)
    #print(wicketsMargins)
    #print(wicketsMargins.aggregate(Max('win_by_wickets')))
    maxValue = wicketsMargins.aggregate(Max('win_by_wickets'))['win_by_wickets__max']
    maxWicketsMargin = {}
    for obj in wicketsMargins:
        if obj['win_by_wickets'] == maxValue:
            maxWicketsMargin = obj
    
    #print(maxWicketsMargin)
    #q2.2
    totalCountTossAndWins = models.IPL.objects.filter(date__year=year, toss_winner = F('winner') ).count()
    #print(totalCountTossAndWins)

    allids=models.IPL.objects.values_list('id', flat=True).filter(date__year=year)
    allids = list(allids)
    #print((allids))
    #print(os.environ.get('MONGO_USER'))
    #print(os.environ.get('MONGO_PASS'))
    uri = 'mongodb+srv://'+os.environ.get('MONGO_USER')+':'+os.environ.get('MONGO_PASS')+'@cluster2.d8upo.mongodb.net/ipl?retryWrites=true&w=majority'
    client = pymongo.MongoClient(uri)
    db = client['ipl']
    cursor4Year = db.get_collection('dummy2').aggregate(
        [
            {
                '$match': {
                    'match_id': {
                        '$in': allids
                    }
                }
            },
            {'$group':{
                '_id': { 'match_id':'$match_id', 'fielder': '$fielder'},
                'count': {'$sum':1}
            }}
        ]
    )

    cursor4Yearbowl = db.get_collection('dummy2').aggregate(
        [
            {
                '$match': {
                    'match_id': {
                        '$in': allids
                    }
                }
            },
            {'$group':{
                '_id': { 'match_id':'$match_id', 'bowler': '$bowler'},
                'totalruns': {'$sum': {'$add' : '$total_runs'} }
            }}
        ]
    )

    cursor4Yearbats = db.get_collection('dummy2').aggregate(
        [
            {
                '$match': {
                    'match_id': {
                        '$in': allids
                    }
                }
            },
            {'$group':{
                '_id': { 'match_id':'$match_id', 'batsman': '$batsman'},
                'totalruns': {'$sum': {'$add' : '$batsman_runs'} }
            }}
        ]
    )
    maxRunsScored = 0
    maxRunsBats = {}
    for player in cursor4Yearbats:
        if (player['_id']['batsman'] != '' and player['totalruns']>maxRunsScored):
            maxRunsScored = player['totalruns']
            maxRunsBats = player
    
    maxRunsBats['id'] = maxRunsBats['_id']
    

    maxRuns=0
    maxRunsBowl = {}
    for player in cursor4Yearbowl:
        if (player['_id']['bowler'] != '' and player['totalruns']>maxRuns):
            maxRuns = player['totalruns']
            maxRunsBowl = player    
    maxRunsBowl['id'] = maxRunsBowl['_id']

    #cursor4PlayerID = db.get_collection('dummy2').find({'fielder': {'$ne': ''}})
    #print(cursor4Year.next())
    maxCatches = {}
    maxCatchesVal = 0
    for player in cursor4Year:
        if (player['_id']['fielder'] != '' and player['count']>maxCatchesVal):
            maxCatchesVal = player['count']
            maxCatches = player
    
    maxCatches['id'] = maxCatches['_id']
    
    #print(maxRunsBowl)
    #q2.3
    
    sendData = {
        'years': dates,
        'topTeam': top4['1'],
        'mostTossWins': maxTossWinsTeam,
        'top4teams': top4.values(),
        'mostPomWins': maxPomWinsTeam,
        'mostTeamWins': maxteamWinsTeam,
        'mostVenueWins': maxVenueWins,
        'percOfBats': percBatQs['bats'] * 100 / totalCount,
        'mostVenue': maxVenue,
        'maxRunMargin': maxRunMargin,
        'maxWicketMargin': maxWicketsMargin,
        'totalCountTossAndWins': totalCountTossAndWins,
        'maxRunsHitMatch': maxRunsBats,
        'maxRunsGiven': maxRunsBowl,
        'maxFielderCatches': maxCatches
    }
    #print(sendData)
    return render(request, 'my_app/new_search.html', sendData)
