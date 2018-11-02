import requests


def geocode(location):

  #高德
  #parameters = {'location': location, 'key': '<高德地图API KEY>'}
  #base = 'http://restapi.amap.com/v3/geocode/regeo';
  #response = requests.get(base, parameters)

  #goole map api
  #street_address 表示精确的街道地址。
  #parameters = {'latlng': location, 'key': '<GOOGLE MAP API KEY>', 'location_type': 'ROOFTOP', 'result_type': 'street_address', 'outputFormat': 'json'}
  parameters = {'latlng': location, 'key': '<高德地图API KEY>'}
  base = 'https://maps.googleapis.com/maps/api/geocode/json';
  response = requests.get(base, parameters)

  #print(response)

  answer = response.json()

  #print(answer)

  #高德
  #return answer['regeocode']['formatted_address']

  #google map api   不同的精度需要调整[2] 里边的数字
   return answer['results'][2]['formatted_address']

  a = geocode('40.714224,-73.961452')

  #b = geocode('43.467448,11.885127')
  print(a)


