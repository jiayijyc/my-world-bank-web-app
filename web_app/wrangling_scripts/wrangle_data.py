import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.colors
from collections import OrderedDict
import requests


# default list of all countries of interest
country_default = OrderedDict([('Canada', 'CAN'), ('United States', 'USA'), 
  ('Brazil', 'BRA'), ('France', 'FRA'), ('India', 'IND'), ('Italy', 'ITA'), 
  ('Germany', 'DEU'), ('United Kingdom', 'GBR'), ('China', 'CHN'), ('Japan', 'JPN')])


def return_figures(countries=country_default):
  """Creates two plotly visualizations using the World Bank API
    Args:
        country_default (dict): list of countries for filtering the data
    Returns:
        list (dict): list containing the four plotly visualizations
  """

  # when the countries variable is empty, use the country_default dictionary
  if not bool(countries):
    countries = country_default

  # prepare filter data for World Bank API
  # the API uses ISO-3 country codes separated by ;
  country_filter = list(countries.values())
  country_filter = [x.lower() for x in country_filter]
  country_filter = ';'.join(country_filter)

  # World Bank indicators of interest for pulling data
  indicators = ['NY.GDP.MKTP.CD', 'SP.POP.GROW']

  data_frames = [] # stores the data frames with the indicator data of interest
  urls = [] # url endpoints for the World Bank API

  # pull data from World Bank API and clean the resulting json
  # results stored in data_frames variable
  for indicator in indicators:
    url = 'http://api.worldbank.org/v2/countries/' + country_filter +\
    '/indicators/' + indicator + '?date=1990:2015&per_page=1000&format=json'
    urls.append(url)

    try:
      r = requests.get(url)
      data = r.json()[1]
    except:
      print('could not load data ', indicator)

    for i, value in enumerate(data):
      value['indicator'] = value['indicator']['value']
      value['country'] = value['country']['value']

    data_frames.append(data)
  
  # first chart plots GDP from 1990 to 2015 in top 10 economies 
  # as a line chart
  graph_one = []
  df_one = pd.DataFrame(data_frames[0])

  # filter and sort values for the visualization
  # filtering plots the countries in decreasing order by their values
  df_one = df_one[(df_one['date'] == '2015') | (df_one['date'] == '1990')]
  df_one.sort_values('value', ascending=False, inplace=True)

  # this  country list is re-used by all the charts to ensure legends have the same
  # order and color
  countrylist = df_one.country.unique().tolist()
  
  for country in countrylist:
      x_val = df_one[df_one['country'] == country].date.tolist()
      y_val =  df_one[df_one['country'] == country].value.tolist()
      graph_one.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country
          )
      )

  layout_one = dict(title = 'Change in GDP( US$) 1990 to 2015',
                xaxis = dict(title = 'Year',
                  autotick=False, tick0=1990, dtick=25),
                yaxis = dict(title = 'GDP( US$)'),
                )

 # seond chart plots population growth from 1990 to 2015 in top 10 economies 
  # as a line chart
  graph_two = []
  df_two = pd.DataFrame(data_frames[1])

  # filter and sort values for the visualization
  # filtering plots the countries in decreasing order by their values
  df_two = df_two[(df_two['date'] == '2015') | (df_two['date'] == '1990')]
  df_two.sort_values('value', ascending=False, inplace=True)

  # this  country list is re-used by all the charts to ensure legends have the same
  # order and color
  countrylist = df_two.country.unique().tolist()
  
  for country in countrylist:
      x_val = df_two[df_two['country'] == country].date.tolist()
      y_val =  df_two[df_two['country'] == country].value.tolist()
      graph_two.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country
          )
      )

  layout_two = dict(title = 'Change in Population Growth (annual %) 1990 to 2015',
                xaxis = dict(title = 'Year',
                  autotick=False, tick0=1990, dtick=25),
                yaxis = dict(title = 'Population Growth (annual %)'),
                )

 
  # append all charts
  figures = []
  figures.append(dict(data=graph_one, layout=layout_one))
  figures.append(dict(data=graph_two, layout=layout_two))


  return figures