import os
import time

import requests
from prometheus_client import start_http_server
from prometheus_client.core import (REGISTRY, CounterMetricFamily,
                                    GaugeMetricFamily)

url = "https://api.covid19india.org/data.json"

responseObj = requests.request("GET", url, headers={}, data = {})
response = responseObj.json()

initialValue = None

class CustomCollector(object):
    def __init__(self):
        pass

    def collect(self):
        global initialValue
        print("Call made")
        
        responseObj = requests.request("GET", url, headers={}, data = {})
        response = responseObj.json()
        

        g = GaugeMetricFamily("total_cases_confirmed", 'Total diagnosed cases in India')
        g.add_metric([], response['statewise'][0]['confirmed'])
        yield g

        if initialValue is None:
            initialValue = response['statewise'][0]['confirmed']

        if initialValue != response['statewise'][0]['confirmed']:
            os.system("say 'There is an update!'")
            initialValue = response['statewise'][0]['confirmed']


        g = GaugeMetricFamily("total_cases_recovered", 'Total recovered cases in India')
        g.add_metric([], response['statewise'][0]['recovered'])
        yield g

        g = GaugeMetricFamily("total_cases_deceased", 'Total deaths in India')
        g.add_metric([], response['statewise'][0]['deaths'])
        yield g

        g = GaugeMetricFamily("total_cases_active", 'Total currently active cases in India')
        g.add_metric([], response['statewise'][0]['active'])
        yield g

        
        for state in response['statewise'][1:]:
            g = GaugeMetricFamily("total_cases_confirmed_by_state", 'Total diagnosed cases in that state', labels=['state'])
            g.add_metric([state['state']], state['confirmed'])
            yield g

            g = GaugeMetricFamily("total_cases_recovered_by_state", 'Total recovered cases in that state', labels=['state'])
            g.add_metric([state['state']], state['recovered'])
            yield g

            g = GaugeMetricFamily("total_cases_deceased_by_state", 'Total deaths in that state', labels=['state'])
            g.add_metric([state['state']], state['deaths'])
            yield g

            g = GaugeMetricFamily("total_cases_active_by_state", 'Total currently active cases in that state', labels=['state'])
            g.add_metric([state['state']], state['active'])
            yield g



if __name__ == '__main__':
    start_http_server(7000)
    REGISTRY.register(CustomCollector())
    while True:
        time.sleep(1)
