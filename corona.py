import time

import requests

from prometheus_client import start_http_server
from prometheus_client.core import (REGISTRY, CounterMetricFamily,
                                    GaugeMetricFamily)


url = "https://api.rootnet.in/covid19-in/stats/latest"

response = requests.request("GET", url, headers={}, data = {})

counter = 1

class CustomCollector(object):
    def __init__(self):
        pass

    def collect(self):
        print("Call made")
        global counter
        responseObj = requests.request("GET", url, headers={}, data = {})
        
        response = responseObj.json()

        g = GaugeMetricFamily("total_cases", 'Total diagnosed cases in India')
        g.add_metric([], response['data']['summary']['total'])
        yield g

        
        for state in response['data']['regional']:
            
            # print(str(state['confirmedCasesIndian'] + state['confirmedCasesForeign']))
            h = GaugeMetricFamily("total_cases_by_state", 'Total diagnosed cases by state', labels = ['state'])
            h.add_metric([state['loc']], float(state['confirmedCasesIndian'] + state['confirmedCasesForeign']))
            yield h

        c = CounterMetricFamily("HttpRequests", 'Help text', labels=['app'])
        c.add_metric(["corona"], counter)

        counter = counter + 1

        yield c


if __name__ == '__main__':
    start_http_server(7000)
    REGISTRY.register(CustomCollector())
    while True:
        time.sleep(1)
