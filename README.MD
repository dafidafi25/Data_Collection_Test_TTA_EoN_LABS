# Coding & Data Collection Take-home Tech Assessment (TTA) by EoN Labs

This is my though process while working on Data Collection TTA

Total Time Used : Approx 30 Hrs

## Installation

Clone Code on git

```bash
git clone https://github.com/dafidafi25/Data_Collection_Test_TTA_EoN_LABS.git
```

After That use the package manager [pip](https://pip.pypa.io/en/stable/) to install request.

```bash
pip install request
```

Or use Requirements.txt

```bash
pip install -r requirements.txt
```

## Usage

```python
python main.py
```

## Working Process

1. Getting to know what is google trends, what data represent in the graph, and trying to figure out if I want to use node js typescript or python, after a lot of readings, I choose python for its flexibility in handling lists or dictionaries. (1 hours)

2. First I used the PyTrends library to try to retrieve data from Google Trends, after a while, I try PyTrends, I noticed that pytrends use panda out of the box, a library that I don't need, and after a while, it feels like too slow, after that I tried to scrape google trends myself, so I can have more flexibility (I spend around 3 - 5 hours)

3. Then I try to figure out how google trends fetch data, I open the network in inspect element tabs, I find there are two processes happening, which is Fetching token using /explore based on what we search, and passing token on search bar to the /multiline, I can use that token that include search data like time, keywords, type, etc. (I Spend 2 hours)

4. After that I try it on the code, at first it always fails, I got 400 error status code for a bad request and 401 status code for not authorized, to handle 401 is because I send parameter that not expected from google trends API, so i trying changing a lot of parameters on google trends to see what kind of parameters google need to get weekly data, daily data and hourly data, to handle 401 request is because i didn't send Goole cookie on request, so i figure it out i need to request on Google trends API to get my cookie, and include it on header in the next request. (I Spend 3 Hours)

5. After success in getting data, i got another error, error 429, which is because i did too much request, i try to figure out how google know that my request is too much, then i article about rotating proxies, and google request limitation, in here i have 2 solutions, after a bunch of request if suddenly google return error 429, i gonna retry next query after 60 seconds, and it works, but it gonna be too long if i want 5 years data, so seconds solution is rotating proxies and use Thread pool with python, after a lot of consideration that maybe it takes too long for me to research about rotating proxy i decided using first solution (I spend more thank 5 hours trying to find other solution)

6. then to get hourly, daily and weekly data, i think i have to use different requests for each CSV, but I think thats gonna take too long time, so I decided to use hourly data to calculate daily data and weekly data. (I spend approx 4 - 8 hours finishing any other elements).
