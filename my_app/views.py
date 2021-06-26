from collections import Counter
from django.db.models.aggregates import Count, Max, Min
import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from . import models

BASE_CRAIGSLIST_URL = 'https://bangalore.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


# Create your views here.
def home(request):
    dates = models.IPL.objects.values().dates('date', 'year')
    print(list(dates))
    for i in list(dates):
        print(i.year)
    setYears ={
      'years': list(dates)
    }
    return render(request, 'base.html', setYears)


def yeardata(request):
    year = request.POST.get('year')
    print('Yo', year)
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
    
    print(top4)
    

    print(top4qs)

    #q2
    tossWins = models.IPL.objects.values('toss_winner').annotate(countoftosswins= Count('toss_winner')).filter(date__year=year)
    maxValue = tossWins.aggregate(Max('countoftosswins'))['countoftosswins__max']
    maxTossWinsTeam = {}
    #print(tossWins.aggregate(Max('countoftosswins')))
    #print(tossWins.aggregate(Max('countoftosswins'))['countoftosswins__max'])
    for obj in tossWins:
        if obj['countoftosswins'] == maxValue:
            maxTossWinsTeam = obj
    #print(maxTossWinsTeam)
    
    
    #q3
    pomWins = models.IPL.objects.values('player_of_match').annotate(countofpomwins= Count('player_of_match')).filter(date__year=year)
    maxValue = pomWins.aggregate(Max('countofpomwins'))['countofpomwins__max']
    maxPomWinsTeam = {}
    for obj in pomWins:
        if obj['countofpomwins'] == maxValue:
            maxPomWinsTeam = obj
    
    #print(maxPomWinsTeam)

    #q4
    teamWins = models.IPL.objects.values('winner').annotate(countofteamwins= Count('winner')).filter(date__year=year)
    maxValue = teamWins.aggregate(Max('countofteamwins'))['countofteamwins__max']
    maxteamWinsTeam = {}
    for obj in teamWins:
        if obj['countofteamwins'] == maxValue:
            maxteamWinsTeam = obj
    
    #print(maxteamWinsTeam)

    #q5
    venueWins = models.IPL.objects.values('venue').annotate(countofvenuewins= Count('venue')).filter(date__year=year, winner=one)
    maxValue = venueWins.aggregate(Max('countofvenuewins'))['countofvenuewins__max']
    maxVenueWins = {}
    for obj in venueWins:
        if obj['countofvenuewins'] == maxValue:
            maxVenueWins = obj
    
    #q6
    totalCount = models.IPL.objects.filter(date__year=year).count()
    percBatQs = models.IPL.objects.filter(date__year=year, toss_decision = 'bat').aggregate(bats = Count('id'))
    # print(percBatQs['bats'] * 100 / totalCount)
    # print(percBatQs['bats'])
    # print(totalCount)

    #print(maxVenueWins)

    #q7
    venue = models.IPL.objects.values('venue').annotate(countofvenue= Count('venue')).filter(date__year=year)
    maxValue = venue.aggregate(Max('countofvenue'))['countofvenue__max']
    maxVenue = {}
    for obj in venue:
        if obj['countofvenue'] == maxValue:
            maxVenue = obj
    

    #q8
    # runMargins = models.IPL.objects.values('result_margin', 'team1', 'team2', 'winner', 'venue').filter(date__year=year, result='runs')
    # print(runMargins)
    # print(runMargins.aggregate(Min('result_margin')))
    # maxValue = runMargins.aggregate(Min('result_margin'))['result_margin__max']
    # maxRunMargin = {}
    # for obj in venueWins:
    #     if obj['result_margin'] == maxValue:
    #         maxRunMargin = obj
    
    # print(maxRunMargin)
    
    sendData = {
        'mostTossWins': maxTossWinsTeam,
        'top4teams': top4,
        'mostPomWins': maxPomWinsTeam,
        'mostTeamWins': maxteamWinsTeam,
        'mostVenueWins': venueWins,
        'percOfBats': percBatQs['bats'] * 100 / totalCount,
        'mostVenue': maxVenue

    }
    return render(request, 'my_app/new_search.html')
# def new_search(request):
#     search = request.POST.get('search')
#     if search is None:
#         search = ""
#         return render(request, 'my_app/new_search.html')
#     else:
#         if models.Search.objects.filter(search=search).exists() is False:
#             models.Search.objects.create(search=search)
#         final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
#         response = requests.get(final_url)
#         data = response.text
#         soup = BeautifulSoup(data, features='html.parser')
#         post_listings = soup.find_all('li', {'class': 'result-row'})
#         final_postings = []

#         for post in post_listings:
#             post_title = post.find(class_='result-title').text
#             post_url = post.find('a').get('href')

#             if post.find(class_='result-price'):
#                 post_price = post.find(class_='result-price').text
#             else:
#                 post_price = 'N/A'

#             if post.find(class_='result-image').get('data-ids'):
#                 post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
#                 post_image_url = BASE_IMAGE_URL.format(post_image_id)
#                 # print(post_image_url)
#             else:
#                 post_image_url = 'https://craigslist.org/images/peace.jpg'

#             final_postings.append((post_title, post_url, post_price, post_image_url))

#         for_front_end = {
#             'search': search,
#             'final_postings': final_postings,
#         }
#         return render(request, 'my_app/new_search.html', for_front_end)
