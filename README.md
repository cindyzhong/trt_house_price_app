# Before You Start

In this session we will build a web app to predict the house price of your property.

## Pre-requisite
* Python 3.6 and above
* Google Maps API: install [googlemaps](https://github.com/googlemaps/google-maps-services-python)
* json
* flask
* pandas
* swat

## Install swat

The SAS SWAT package is a Python interface to the SAS Cloud Analytic Services (CAS) engine (the centerpiece of the SAS Viya framework). With this package, you can load and analyze data sets of any size on your desktop or in the cloud. Since CAS can be used on a local desktop or in a hosted cloud environment, you can analyze extremely large data sets using as much processing power as you need, while still retaining the ease-of-use of Python on the client side.

* From the python-swat repository: install [python-swat](https://github.com/sassoftware/python-swat).


## Create file for credentials

In your $HOME directory, create a csv file containing your credentials
|google_api_key |Your Google Earth API Token|
|---|---|
|casuser | your cas username provided |
|---|---|
|password | your cas password provided |

## Test your CAS connection

Once you have installed swat package, make a connection to the server. (Note: the connection may not work for some Scotia IP addresses, if it does not work, try connecting using a Non-Scotia network).

```python
import swat
import pandas as pd

creds = pd.read_csv('~/creds.csv', header=None)
username = creds.iloc[1,1]
password = creds.iloc[2,1]

conn = swat.CAS('http://13.88.252.54/cas-shared-default-http/',5570, username, password)
conn.userinfo()
```

If this is successful, you should be able to see a response from the server:
```
§ userInfo
{'anonymous': False, 'groups': ['sasadmin', 'DataBuilders', 'openid', 'SASScoreUsers', 'SASAdministrators'], 'guest': False, 'hostAccount': True, 'providedName': 'cindy', 'providerName': 'OAuth/External PAM', 'uniqueId': 'cindy', 'userId': 'cindy'}
elapsed 0.000495s · user 0.000271s · sys 0.000131s · mem 0.194MB
```

## Test your Google Maps Geocoding

We will use the geocoding service from Google Maps API. Test if you can successfully get response from the following call.
```python
import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key)

# Geocoding an address
gmaps.geocode('M5A 1K7')
```

If this is successful, you should be able to see a response from the server:
```
[{'address_components': [{'long_name': 'M5A 1K7',
    'short_name': 'M5A 1K7',
    'types': ['postal_code']},
   {'long_name': 'Old Toronto',
    'short_name': 'Old Toronto',
    'types': ['political', 'sublocality', 'sublocality_level_1']},
   {'long_name': 'Toronto',
    'short_name': 'Toronto',
    'types': ['locality', 'political']},
   {'long_name': 'Toronto Division',
    'short_name': 'Toronto Division',
    'types': ['administrative_area_level_2', 'political']},
   {'long_name': 'Ontario',
    'short_name': 'ON',
    'types': ['administrative_area_level_1', 'political']},
   {'long_name': 'Canada',
    'short_name': 'CA',
    'types': ['country', 'political']}],
  'formatted_address': 'Toronto, ON M5A 1K7, Canada',
  'geometry': {'bounds': {'northeast': {'lat': 43.65235149999999,
     'lng': -79.3652587},
    'southwest': {'lat': 43.6517379, 'lng': -79.36616839999999}},
   'location': {'lat': 43.65200369999999, 'lng': -79.36582750000001},
   'location_type': 'APPROXIMATE',
   'viewport': {'northeast': {'lat': 43.65339368029149,
     'lng': -79.36436456970848},
    'southwest': {'lat': 43.65069571970849, 'lng': -79.3670625302915}}},
  'place_id': 'ChIJYY360DvL1IkR3AR8KQF55uE',
  'types': ['postal_code']}]
```
