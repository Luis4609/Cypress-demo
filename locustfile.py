# Author ashsepra@gmail.com
# This load test for example
# Scope on load test at wikipedia

import time
from locust import HttpUser, TaskSet, task, between, events
from jtl_listener import JtlListener

class SubClassTest(TaskSet):

    @task
    def main_page(self):
        self.client.get('/wiki/Halaman_Utama')

    @task(2)
    def perihal_page(self):
        self.client.get('/wiki/Wikipedia:Perihal')

@events.init.add_listener
def on_locust_init(environment, **_kwargs):
     JtlListener(env=environment,  project_name="sorry-cypress",
                scenario_name="locust test",
                hostname="hostname",
                backend_url="http://localhost:2020")


class MainClassTest(HttpUser):
    tasks = [SubClassTest]
    wait_time = between(5, 10)
    