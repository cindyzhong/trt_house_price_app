from flask import Flask,redirect, render_template, request
import json
import pandas as pd
app = Flask(__name__)

@app.route('/')

def main():
  return render_template('house_price_api.html')

# app vars:
cas_library = "Public"
model_name = "_14DRK27R6VW68138RUSDZ6SQRJ"  # filename of astore model

# credentials:
creds = pd.read_csv('~/creds.csv', header=None)
google_api_key = creds.iloc[0,1]
casuser = creds.iloc[1,1]
password = creds.iloc[2,1]

@app.route('/score',methods=['POST'])

def score():
  import pandas as pd
  import googlemaps
  gmaps = googlemaps.Client(key=google_api_key)
  # read the posted values from the UI
  _NAME = request.form['customerName']
  _HOUSETYPE = request.form['House_Type']
  _POSTALCODE = request.form['Postal_Code']
  _APPRSQFT = request.form['Approximate_Sqft']
  _BEDROOMS = request.form['Bedrooms']
  _WASHROOMS = request.form['Washrooms']
  _PAKRINGS = request.form['ParkSpcs']
  #print (str(_POSTALCODE))
  # To Do: Connect to google maps API to get the longitude and latitude from postal code
  geocode_result = gmaps.geocode(_POSTALCODE + 'Canada')
  print (geocode_result)
  location = geocode_result[0]['geometry']['location']
  latitude = location['lat']
  longitude = location['lng']
  #latitude = 47
  #longitude = -71

  # Convert inputs to pandas dataframe and upload to CAS
  df = pd.DataFrame(data = [[1,1,1,1,1,1],[_APPRSQFT,_BEDROOMS,latitude,longitude,_PAKRINGS,_HOUSETYPE,_WASHROOMS]],columns = ["Approximate_Sqft","Bedrooms_Main","Latitude","Longitude","ParkSpcs","Type","Washrooms"])
  scoretbl = cas_session.upload_frame(df, casout=dict(name="input",replace=True,caslib=cas_library))

  # Score the inputs using astore
  results = cas_session.score(
  rstore=dict(name=model_name,caslib=cas_library),
  table=dict(name="input",caslib=cas_library),
  out=dict(name="output",caslib=cas_library,replace=True)
  )

  # Give the probability of having a good loan
  output = cas_session.fetch(dict(name = 'output', caslib = cas_library))['Fetch'].iloc[1,0]

  output_upper = output * 1.15
  output_lower = output * 0.85


#  if DEBUG:
#   print(output)
#  output_msg = _NAME + ', Your predicted house price is :' + '${:,.2f}'.format(output)
  output_msg = _NAME + ', Your predicted house price is around:' + '${:,.2f}'.format(output_lower) + ' to ' + '${:,.2f}'.format(output_upper)
  return '<font size=5 color="black"><b>' + output_msg + '</b></font>'

if __name__ == "__main__":
  DEBUG = True

  # Import Python packages
  import swat
  import pandas as pd

  # Start CAS Session
  cas_session = conn = swat.CAS('http://13.88.252.54/cas-shared-default-http/',5570, casuser, password)

  # Load astore actionset for scoring
  cas_session.loadactionset('astore')

  # Run the application
  app.run(host='0.0.0.0', debug=DEBUG)
