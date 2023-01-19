import threading
import requests as req
from bs4 import BeautifulSoup
import time
import json
import re

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Grape(object):
    def __init__(self):
        self.max_threads = 220
        return print(f'{colors.OKGREEN}INFO{colors.ENDC}:     Grape Module initalized.')

    def start_nick_checker(self, nicks: list, region):
        if len(nicks) > self.max_threads:
            return {"error": True, "message": "you can't check more than 220 nicks."}
        else:
            self.live_nicks = []
            self.die_nicks = []
            self.available_nicks = []
            self.banned_nicks = []
            self.nicks = nicks
            self.region = region
            self.threads = []
            start_time = time.time()
            for i in range(len(self.nicks)):
                for nick in self.nicks:
                    t = threading.Thread(target=self.nick_checker, args=(
                        str(nick).strip().capitalize(),
                    ))
                    t.daemon = True
                    self.threads.append(t)
            for i in range(len(self.nicks)):
                self.threads[i].start()

            for i in range(len(self.nicks)):
                self.threads[i].join()


            return {
                "availables": self.available_nicks,
                "lives": self.live_nicks,
                "dies": self.die_nicks,
                "banneds": self.banned_nicks,
                "checker_speed": "{:.1f} seconds".format((time.time() - start_time))
            }
    def nick_checker(self, nick):
        nick = nick.lower().replace("&", " ")   
        html = req.get(f"https://lols.gg/en/name/checker/{self.region.lower()}/{nick}/")
        soup = BeautifulSoup(html.text, 'html.parser')
        nick_expires = soup.find("h4").text.capitalize()
        response = str(nick_expires).strip().replace(" ", "").capitalize()
        
        if response == f"{nick.capitalize()}isavailable!":
            self.available_nicks.append(f"{nick} is available.")
        elif response == f"{nick.capitalize()}isprobablyavailable!":
            self.banned_nicks.append(f"{nick} is probably banned.")
        elif response.endswith("days.") == True:
            available_date = re.findall('[0-9]+', response)
            if int(available_date[0]) > 50:
                self.die_nicks.append(
                    f"{nick} will be available in {available_date[0]} days.")
            else:
                self.live_nicks.append(
                    f"{nick} will be available in {available_date[0]} days.")
