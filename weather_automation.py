__author__ = 'suriyakumar.s2'

import json,re,sys,requests,urllib as ul, urlparse as up,pandas as pd
from datetime import date
reload(sys)
sys.setdefaultencoding('UTF-8')

class test_page():
    def dataExtraction(self,soup,html_source):
        dataList = []
        for weatherName in soup:
            data = {}
            InputCountryName = re.findall('q=([^"]+)',url)[0]
            cityName = weatherName['name']
            apiKey = re.findall('key=.*?&',url)[0].replace('&','').replace('key=','')
            forecasturl = 'http://api.weatherapi.com/v1/forecast.json?key={}&q={}&days=5&aqi=yes&alerts=yes'.format(str(apiKey),str(cityName))    ####################forming forecasting url
            header = {"Host": "api.weatherapi.com","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"}
            responseUrl = requests.get(forecasturl, headers=header).content
            if responseUrl.__contains__(InputCountryName):
                regionsData = json.loads(responseUrl)
                data['Name'] = regionsData['location']['name']+ ', ' + regionsData['location']['country']
                data['Coordinates'] = 'latitude: ' + str(regionsData['location']['lat']) + ', longitude: ' + str(regionsData['location']['lon'])
                tempData = regionsData['forecast']['forecastday']
                temList = []
                for i in tempData:
                    Temp = i['day']['avgtemp_f']
                    temList.append(str(Temp))
                avgT = sum(map(float,temList)) / 3
                data['averageTemperature'] = "{:.2f}".format(avgT)
                curforecasturl = 'http://api.weatherapi.com/v1/current.json?key={}&q={}&aqi=yes'.format(str(apiKey), str(cityName))
                curforecasturl = requests.get(curforecasturl).content
                if responseUrl.__contains__(InputCountryName):
                    curTempData = json.loads(curforecasturl)
                    data['currentTemperature'] = curTempData['current']['temp_f']
            dataList.append(data)
        return dataList

def parse(html_source):
    soup = json.loads(html_source)
    test_page_object = test_page()
    output = test_page_object.dataExtraction(soup,html_source)
    print json.dumps(output,indent=2)
    return output

if __name__ == '__main__':
    url = 'http://api.weatherapi.com/v1/search.json?key=5dad4c31e4434311a8e132245222103&q=Germany'
    header = {"Host": "api.weatherapi.com","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"}
    urlResponse = requests.get(url,headers=header).content
    parse(urlResponse)
