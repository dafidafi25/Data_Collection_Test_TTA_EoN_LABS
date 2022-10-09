from time import sleep
import urllib
import json
import requests

class GoogleTrendsAPI():
    # List Of Google Trends API , Directly Find It From Network Menu in browser
    ## NID COOKIES from google, Unique
    ## BASE_REQUEST To Get Token, and inform other request what we search based on token we get from base request
    ## INTEREST_OVER_TIME to Query trends based on what we search before

    COOKIES = 'https://trends.google.com/'
    BASE_REQUEST = f'https://trends.google.com/trends/api/explore/'
    INTEREST_OVER_TIME = f'https://trends.google.com/trends/api/widgetdata/multiline/'

    def __init__(self) -> None:
        # Getting Cookies from google on first initate data
        self.jar = requests.get("https://trends.google.com/").cookies.get_dict()
        self.headers = {"Cookie": f'NID={self.jar["NID"]}'}
        self.token = None
        pass

    def QueryTrends(self,keyword="bitcoin", time ='/m/05p0rrx'):
        # Preparing Request
        item = json.dumps({"comparisonItem":[{"keyword":keyword,"geo":"","time":time}],"category":0,"property":""})
        params = {'tz':-420,'tz':-420}
        url = f'https://trends.google.com/trends/api/explore?req={item}'

        # Send Request Expect get token from response
        data = requests.get(url,headers=self.headers, params=params)
        retry = 0 
        cnt = 0 
        
        # Check if google gives 429 status code, which mean too much request
        # Retrying request, 3 times maximum, with each iteration is delayed 60 seconds
        # 60 Seconds is to get request quota, we can handle this wether delay it
        # Or changing proxy, in here i just delay it
        while (data.status_code == 429) or data.status_code == 500:
            if retry == 3 : break
            print(f'Too Many request on token {time} Retrying number {cnt}...')
            sleep(60)
            data = requests.get(url,headers=self.headers, params=params)
            retry+=1
            cnt+=1
        
        # Check if there is any problem beside 429 status code
        # I check only if status code is above 300 indicate not success
        if data.status_code >= 300 : 
            print(data.status_code)
            return False
        return json.loads(data.text[4:len(data.text)])['widgets']

    def InterestOverTime(self,keyword='bitcoin', time='today+5-y'):
        # Getting Tokens, since we need to get hourly data, only on 1 week request i got hourly data
        # so i iteratively request on every week and calculate programmatically on daily and weekly value
        # widgets -> when we request on google trends api after search query,
        # Google trends gonnda response based on widget in google trends API
        # first widget that show graph, widget based on country, related topic, related query
        # in here i autcomatically choose widget interest, in the widgets also includes token
        widgets = self.QueryTrends(keyword,time)

        # Check if widget return boolean which is something went wrong
        if isinstance(widgets,bool) : return False 
        params_1 = None

        # in here i autcomatically choose widget interest
        for widget in widgets:
            if "title" not in widget: continue
            # as on 09-08-2022(dd-mm-yy) this widget is named interest overtime, data that used on graph by google trends
            if widget["title"] == "Interest over time":
                params_1 = {
                            "req":widget["request"],
                            "token":widget["token"],
                            "tz":-420
                            }

        # If somehow google change its backend, just to make sure params 1 is filled
        if params_1 is not None:
            # Creating Request
            params_1["req"] = json.dumps(params_1["req"],separators=(',', ':'))
            params_1 = urllib.parse.urlencode(params_1).replace("+", "%20")
            csv_url = 'https://trends.google.com/trends/api/widgetdata/multiline?' + params_1
            result = requests.get(csv_url,headers=self.headers)
            retry = 0 
      
            cnt = 0 

            # Retrying on 60 seconds if google returns too much requests
            while (result.status_code == 429) or result.status_code == 500:
                if retry == 3 : break
                print(f'Too Many request on time {time} Retrying number {cnt} ...')
                sleep(60)
                result = requests.get(csv_url,headers=self.headers)
                retry+=1
                cnt+=1

            if result.status_code <=299:
                json_data = json.loads(result.text[5:len(result.text)])['default']['timelineData']
                
                return json_data
            else:
                print(result.status_code)
                return False


if __name__ == "__main__":
   test = GoogleTrendsAPI()

   test.INTEREST_OVER_TIME()