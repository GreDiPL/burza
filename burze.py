#!/usr/bin/env python
# coding=utf-8
#
__author__ = 'Grzegorz Deneka'
__license__ = "GPL"
__status__ = "Proof of concept - prototype"
__version__ = "0.1"

from SOAPpy import WSDL
import configparser
import sys

#wsdl_file = 'https://burze.dzis.net/soap.php?WSDL'
#key = 'ASDASDASD123123123'
#city = 'warszawa'
#range_detect = 25  # in km
config_file="burze.ini"

def get_config(filename, section):
    dict1 = {}
    config = configparser.ConfigParser()
    config.read(filename)
#    return config.get(value)

def burze_api(key, wsdl_file, city, detect_range):
    server = WSDL.Proxy(wsdl_file)
    xy = server.miejscowosc(city, key)
    ostrzezenia = server.ostrzezenia_pogodowe(xy.x, xy.y, key)
    burza = server.szukaj_burzy(xy.x, xy.y, detect_range, key)
    return [ostrzezenia, burza]


def print_burza(burza):
    print "=== Wykrywanie burzy ==="
    if burza['liczba'] == 0:
        print "Brak burzy"
    else:
        print "Kierunek: ", str(burza['kierunek'])
        print "Liczba: ", str(burza['liczba'])
        print "Odleglosc: ", str(burza['odleglosc']), "km"
        print "Okres: ", str(burza['okres']), "min"


def print_ostrzezenia(ostrzezenia):
    print "=== Ostrzezenia pogodowe==="
    print "Mroz: {0} {1} {2}".format(ostrzezenia['mroz'], ostrzezenia['mroz_od_dnia'], ostrzezenia['mroz_od_dnia'])
    print "Upal: {0} {1} {2}".format(ostrzezenia['upal'], ostrzezenia['upal_od_dnia'], ostrzezenia['upal_od_dnia'])
    print "Wiatr: {0} {1} {2}".format(ostrzezenia['wiatr'], ostrzezenia['wiatr_od_dnia'], ostrzezenia['wiatr_od_dnia'])
    print "Opad: {0} {1} {2}".format(ostrzezenia['opad'], ostrzezenia['opad_od_dnia'], ostrzezenia['opad_od_dnia'])
    print "Burza: {0} {1} {2}".format(ostrzezenia['burza'], ostrzezenia['burza_od_dnia'], ostrzezenia['burza_od_dnia'])
    print "Traba: {0} {1} {2}".format(ostrzezenia['traba'], ostrzezenia['traba_od_dnia'], ostrzezenia['traba_od_dnia'])


def main():
    config = configparser.ConfigParser()
    config.read(config_file)

    ostrzezenia, burza = burze_api(config.get('burze.dzis.net', 'apikey'), config.get('burze.dzis.net', 'wsdl_file'), config.get('burze.dzis.net', 'city'), config.get('burze.dzis.net', 'range_detect'))
    print_burza(burza)
    print_ostrzezenia(ostrzezenia)

if __name__ == "__main__":
    main()
