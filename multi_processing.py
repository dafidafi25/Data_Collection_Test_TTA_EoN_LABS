import concurrent.futures
import random
from time import sleep
import urllib.request

URLS = [2,
        1,
        3,
        5,
        6,
        2,
        1,
        3,
        5,
        6]

# Retrieve a single page and report the URL and contents
def load_url(url, timeout):
    wait  = random.randint(0,5)
    print(f'waiting for : {wait}')
    sleep(wait)
    return url

# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
    all_results = []
    for i in executor.map(future_to_url):
            all_results.append(i)
    print('Waiting for tasks to complete...')
    concurrent.futures.wait(future_to_url)
    print('All tasks are done!')
    print(all_results)
    executor.shutdown() 