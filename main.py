import datetime
import concurrent.futures
from CsvGenerator import Csv_Writter
from GoogleTrends import GoogleTrendsAPI

# Routines to load trends
def load_trends(time='today+5-y',keyword="/m/05p0rrx"):
    ## Define Google Trends API
    # Due to performance issues i think i dont need panda
    # or pytrends package, and handle things myself
    trends = GoogleTrendsAPI()
    data = trends.InterestOverTime(time=time,keyword=keyword)

    # Check if something is wrong, etc : status code 500, or 400
    # if status code is 429, program gonna retry it max 3 times with delay on each try is 60 seconds
    # due too much request on google trends API
    if isinstance(data,bool): 
        print("Something went wrong ....")
        return False
    
    # Initiate hourly, daily and weekly request
    hourly = Csv_Writter(Csv_Writter.HOURLY)
    daily = Csv_Writter(Csv_Writter.DAILY)
    weekly = Csv_Writter(Csv_Writter.WEEKLY)
    
    # Create daily and weekly variable to calculate based on hourly data
    daily_val, daily_date, daily_cnt = 0, "", 0
    weekly_val, weekly_date, weekly_cnt = 0, "", 0
    
    ## Start Process too calculate daily value and wekkly value, also
    #  also write data on each csv files
    for row in data:
        # Debug purpose
        # print(f'{row["formattedTime"]} value : {row["value"]} daily : {daily_date} {daily_cnt} weekly : {weekly_date}')
        # print(f'daily : {daily_date} {daily_cnt} weekly :  {weekly_date} {weekly_cnt}')

        # Writing into csv named hourlt.csv inside results folder
        hourly.write_data(row)

        # Counting if 24 hours passed and processing data needed to append data to daily .csv
        if daily_cnt >= 24:
            # Debug Purpose
            #print(f' Daily Date : {daily_date} with value : {daily_val}')

            # Reset Daily Counting
            daily_cnt=0

            # Getting Average Value for 24 hours accumulated data
            daily_val = daily_val / 24

            # Writing data on daily.csv
            daily.write_data(dict({'formattedTime' : daily_date, 'value': [daily_val]}))
            
            # Reset Daily data
            daily_val = 0 

        # Counting if 168 hours which is 1 week and processing data needed to append data to daily .csv
        if weekly_cnt >= 168:
            # Debug Purpose
            #print(f' Weekly Date : {weekly_date} with value : {weekly_val}')

            # Reset Weekly Counting
            weekly_cnt=0

            # Getting Average Value for 168 hour (1-Week) accumulated data
            weekly_val = weekly_val / 168

            # Writing Data on weekly.csv
            weekly.write_data(dict({'formattedTime' : weekly_date, 'value': [weekly_val]}))

            # Reset Daily data
            weekly_val = 0 

        # Getting date on first cnt of daily and weekly
        daily_date = row['formattedTime'] if daily_cnt == 0 else daily_date
        weekly_date = row['formattedTime'] if weekly_cnt == 0 else weekly_date

        # Accumulating value
        daily_val = daily_val + row['value'][0]
        weekly_val = weekly_val + row['value'][0]
        
        # Counting Daily and weekly on every hours
        daily_cnt =  daily_cnt +  1
        weekly_cnt = weekly_cnt + 1    

    return True 


# To reset daily, hourly, and weekly files
def reset_files():
    hourly_reset = Csv_Writter(Csv_Writter.HOURLY)
    hourly_reset.reset_files()
    daily_reset = Csv_Writter(Csv_Writter.DAILY)
    daily_reset.reset_files()
    weekly_reset = Csv_Writter(Csv_Writter.WEEKLY)
    weekly_reset.reset_files()

if __name__=="__main__":

    ## Since we need to get hourly, daily and weekly
    # I decided to get hourly data and calculate average value on daily basis and weekly basis
    start_date = datetime.date(2015, 1, 1)
    end_date = datetime.date.today()
    weekly_range = datetime.timedelta(days=7)
    daily_range  = datetime.timedelta(days=1)
    dates = []

    reset_files()

    while (start_date <= end_date):
        first_date = start_date 
        start_date += weekly_range
        if(start_date <= end_date):
            dates.append(f'{first_date}T00 {start_date}T00') 

    ## In hear i mean to start Querying with Thread pool Executer to get data
    # after a lot of consideration i decided only work with 1 workers, since
    # using Thread pool executor without rotating proxy is kind a useless because of
    # google Maximum Request

    # I Decide to leave as it is now with max workers 1
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future_to_url = {executor.submit(load_trends,date,'bitcoin'): date for date in dates}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
            except Exception as exc:
                pass
        
        executor.shutdown() 