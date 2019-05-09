#!/usr/bin/python

#---------------------------------------------------------
# Project         : Digital Manufacturing on the Shoestring
# Program name    : Stores IP into a cloud-based CouchDB 
# Author          : German Terrazas (gt401@cam.ac.uk)
# Date created    : 20190501
# Purpose         : This programs reads the current wifi IP.
#                   If the IP value is new, then it stores 
#                   in a cloud-based CouchDB. The program is
#                   scheduled to run when the RPi OS boots 
#                   and also every hour o'clock.
# Revision history:
# Date      Author      Ref      Comment
# 20190501  gt401        1       Added this header
#---------------------------------------------------------

import os
import couchdb
import netifaces as ni
import datetime
from ConfigParser import *

ADDRESS_FILE = ''
inifilename = '/home/pi/3dprinter/storeip.ini'
username ="" 
password = ''
couchIP = ''
couchPort = ''
couchTable = '' 

def detect_ip_change():
    blnDelta = False
    currIp = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
    if not os.path.isfile(ADDRESS_FILE):
        persist_ip('127.0.0.1')
    oldIp = read_old_ip()
    if currIp != oldIp:
      blnDelta = True
      persist_ip(currIp)
    return (blnDelta, currIp)
# [detect_ip_change ends]


def persist_ip(ip):
    f = open(ADDRESS_FILE, 'w')
    f.write(ip)
    f.close()
# [persist_ip ends]


def read_old_ip():
    f = open(ADDRESS_FILE, 'r')
    oldIp = f.read()
    f.close()
    return oldIp
# [read_old_ip ends]


def read_ini(filename):
  config = ConfigParser()
  config.read(filename)
  config.sections()
  global username 
  username = config.get('CREDENTIALS','username')
  global password 
  password = config.get('CREDENTIALS','password')
  global couchIP 
  couchIP = config.get('SERVER', 'couchIP')
  global couchPort 
  couchPort = config.get('SERVER', 'couchPort')
  global couchTable 
  couchTable = config.get('SERVER', 'couchTable')
  global ADDRESS_FILE
  ADDRESS_FILE = config.get('LOCAL', 'oldIPAddresses')
# [read_ini end]


def store_IP(table, IP):
  timestamp = datetime.datetime.now().isoformat()
  doc = {'timestamp': timestamp, 'ip':IP}
  table.save(doc)
# [store_IP end]


def prepare_couchdb():
  couch=couchdb.Server("http://"+username+":"+password+"@"+couchIP+":"+couchPort)
  global couchTable
  table = couch[couchTable]
  return table 
# [prepare_couchdb end]


def get_Host_IP():
  try:
     ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
     return ip
  except:
     print("Unable to get values")
# [get_Host_IP end] 


def main():
  read_ini(inifilename) 
  deltaTuple = detect_ip_change()
  if deltaTuple[0] is True:
    ip = deltaTuple[1] #get_Host_IP()
    table = prepare_couchdb()
    store_IP(table, ip)
    print "New IP stored"
  else:
        print "Same IP as before."
# [main end]


if __name__ == '__main__':
    main()

