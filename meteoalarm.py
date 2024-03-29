#!/usr/bin/python3

# Copyright (c) 2021 SQ9MDD Rysiek Labus
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

# DATA SOURCE meteoalarm.eu
# look for metegram and find" img with alt="awt:6 level:1"
#   Awarness Type:
#   1       wind
#   2       snow / ice
#   3       thunderstorm
#   4       fog
#   5       extreme high temperature
#   6       extreme low temperature
#   7       coastal event
#   8       Forest fire
#   9       Avalanches
#   10      Rain
#   11      Flood
#   12      Rain-Flood

#   Awarness level:
#   0       No data or invalid data
#   1       GREEN No particular awareness of the weather is required
#   2       YELLOW The weather is potentially dangerous. The weather phenomena that have been forecast are not unusual, but be attentive if you intend to practice activities exposed to meteorological risks
#   3       ORANGE The weather is dangerous. Unusual meteorological phenomena have been forecast. Damage and casualties are likely to happen
#   4       RED The weather is very dangerous. Exceptionally intense meteorological phenomena have been forecast. Major damage and accidents are likely, in many cases with threat to life and limb, over a wide area.

# CHANGELOG
# 20210707 - changing feed source according to new meteoalarm interface (https://feeds.meteoalarm.org/) tnx for info Cesar ;-)
# 20220118 - deploy fixes from SQ7LQU
# 20230807 - migrating to python3
# ----------------------configuration----------------------------- #
rss_url = 'https://feeds.meteoalarm.org/feeds/meteoalarm-legacy-rss-poland'         # put here valid RSS url for your country from meteoalarm.eu
#rss_county = 'Mazowieckie Province Warszawa County'                                 # region or country name exactly as it is in RSS
rss_county = 'Zachodniopomorskie Province Świnoujście County'

from locale import pl_awt as def_awt
from locale import pl_lvl as def_lvl
# ----------------------configuration----------------------------- #

from urllib.request import urlopen

def set_label_for_alert(alert = 0):
    if(alert == 0):
        return()
    else:
        return(def_lvl[alert])

def set_label_for_awerness(awt = 0):
    if(awt == 0):
        return()
    else:
        return(def_awt[awt])

def get_data_and_extract_alerts(rss_url,rss_county):
    try:
        response = urlopen(rss_url)
        text = response.read().decode('utf-8')
        county_code_pos = text.find(rss_county)
        awt_pos = text.find("awt:",county_code_pos) + 4
        lvl_pos = text.find("level:",county_code_pos) + 6
        awt = text[awt_pos:(awt_pos + 2)]        # AWT
        lvl = text[lvl_pos:(lvl_pos + 1)]        # LVL
        return_data = [int(awt),int(lvl)]        # awt,lvl
        return(return_data)
    except:
        return_data = [0,0]
        return()

try:
    curr_alert_data = get_data_and_extract_alerts(rss_url,rss_county)
    if(curr_alert_data[1] > 1):
        status_frame = ">" + set_label_for_alert(curr_alert_data[1]) + ' ' + set_label_for_awerness(curr_alert_data[0])
    else:
        status_frame = ">" + set_label_for_alert(curr_alert_data[1])
    print(status_frame)
except:
    pass
