#!/usr/bin/python

#-------------------------------------------------------
# Project         : Manufacturing on the Shoestring
# Program name    : Tweets from RPi
# Author          : German Terrazas (gt401@cam.ac.uk)
# Date created    : 20190429
# Purpose         : This program tweets the current wifi IP
# 
# Revision history:
# Date        Modifier      Ref      Comment
# 20190430    gt401          1       Added this header
# 20190509    gt401          2       Moved keys to ini file
# ------------------------------------------------------

from twython import Twython
import netifaces as ni
import random
from ConfigParser import *

filename = '/home/pi/3dprinter/tweetip.ini'
nouns = ["mouse", "rabbit", "elephant", "ox", "zebra", "llama", "sheep", "coyote"]
verbs = ["runs", "jumps", "drives", "stays", "crosses", "writes", "sleeps", "tangoes"]
adv   = ["crazily", "merrily", "dutifully", "dizzy", "steady", "peacefuly", "quickly", "hefty"]

def get_Host_name_IP():
  try:
     ip=ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
     config = ConfigParser()
     config.read(filename)
     config.sections()
     C_key = config.get('CREDENTIALS','C_key')
     C_secret = config.get('CREDENTIALS','C_secret')
     A_token = config.get('CREDENTIALS','A_token')
     A_secret = config.get('CREDENTIALS','A_secret')
     myTweet = Twython(C_key,C_secret,A_token,A_secret)
     ranNum = random.randrange(0,7)
     random.shuffle(nouns)
     random.shuffle(verbs)
     random.shuffle(adv)
     phrase = adv[ranNum]+' '+nouns[ranNum]+' '+verbs[ranNum]+' '+adv[ranNum] 
     print(phrase)
     myTweet.update_status(status=("#3dpdownstairs "+phrase+" "+ip))
  except:
     print("Unable to get values")

get_Host_name_IP()
 
