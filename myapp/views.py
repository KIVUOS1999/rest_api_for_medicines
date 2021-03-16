from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
import json

from bs4 import *
import requests as rp
import os
from msedge.selenium_tools import *
import time
from tqdm import tqdm
import pickle
import numpy as np
import psycopg2 as ps
import random

options = EdgeOptions()
options.use_chromium = True
options.add_argument("headless")
driver = Edge(options = options)

@api_view(['POST'])
def search(string):
    try:
        data = {'name':[], 'description':[], 'url':[], 'price':[]}
        containers_error = ''
        key = string.body
        key = str(key)[1:]
        key = '%20'.join(key.split(' '))
        
        driver.get('https://www.1mg.com/search/all?name='+key[1:-1])
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        containers_error = soup.find('li', {'class':'list-suggest'})
        
        if containers_error == None:
            containers = soup.find_all('div', {'class':"style__horizontal-card___1Zwmt"})
            containers_grid = soup.find_all('div', {'class':"col-md-3 col-sm-4 col-xs-6 style__container___jkjS2"})
            #for list-view
            for i in containers:
                try:
                    name = i.find('span', {'class':'style__pro-title___3zxNC'}).text
                except:
                    print('name not correct')
                    break
                try:
                    description = i.find('div', {'class':'style__pack-size___254Cd'}).text
                except:
                    description = ''
                try:
                    price = i.find('div', {'class':'style__product-pricing___1tj_E'}).text
                except:
                    price = ''
                try:
                    url = i.find('a')['href']
                except:
                    url = ''
                data['name'].append(name)
                data['description'].append(description )
                data['url'].append(url)
                data['price'].append(price)

            #for grid-view
            for i in containers_grid:
                try:
                    name = i.find('div', {'class':'style__pro-title___3G3rr'}).text
                except:
                    print('name not correct')
                    break
                try:
                    description = i.find('div', {'class':'style__pack-size___3jScl'}).text
                except:
                    description = ''
                try:
                    price = i.find('div', {'class':'style__price-tag___KzOkY'}).text
                except:
                    price = ''
                try:
                    url = i.find('a')['href']
                except:
                    url = ''
                data['name'].append(name)
                data['description'].append(description )
                data['url'].append(url)
                data['price'].append(price)
            
        #for error-typing          


        return JsonResponse(json.dumps(data, indent = 4), safe = False)
    
    except ValueError as e:
        return Response(e.args[0])