#! /usr/bin/env python3
import os

import urllib.request
import feedparser
import time

from bs4 import BeautifulSoup
import datetime
from dateutil.parser import parse
import notify2 as notify
import re
import shutil

def getDateTime(struct_datetime):
      ''' Parse datetime available '''

      movie_time = time.mktime(struct_datetime)
      published_date = datetime.datetime.fromtimestamp(movie_time)
      return published_date

def saveMovieImages(img_movie, movie_image_src):
      ''' Save images of the movies in folder '''
      if not os.path.exists(img_movie):
            os.makedirs(img_movie)

      opener = urllib.request.URLopener()
      opener.addheader('User-Agent', 'whatever')
      opener.retrieve(movie_image_src, os.path.join(img_movie, os.path.basename("cover.jpg")))


def invoke_feed():
      ''' This gets the feeds from YTS website '''

      dir_path = os.path.dirname(os.path.realpath(__file__))
      torrent_feeds = feedparser.parse("https://yts.ag/rss")

      i=1
      torrent_released = dict()
      movie_image = []
      img_path = dir_path+"/img/"

      # remove the directry if exists
      if os.path.exists(img_path):
            shutil.rmtree(img_path)


      for entry in torrent_feeds.entries:
            
            published_date = getDateTime(entry.published_parsed)

            #get title and description
            move_description = ''
            torrent_title = entry.title

            #get description
            desc = entry.summary_detail.value

            #convert to beautiful soup object
            soup = BeautifulSoup(desc)

            # get image of the movie
            movie_image_src = soup.findAll('img')[0].get('src')

            #remove link and image tag
            for link in soup.findAll(['a','img']):
                  link.unwrap()

            #remove <br>
            for description in soup.find_all('body'):
                  move_description = "\n".join(description.strings)

            # format the data
            description = move_description.split("\n")
            movie_desc = description[0]+"\n"+description[1]+"\n"+description[2]+"\n"+description[3]
            img_movie = img_path + torrent_title

            # if published today then store the details
            if(published_date.date() == datetime.datetime.today().date()):
                  # save images
                  saveMovieImages(img_movie, movie_image_src)
                  pub_date = published_date.strftime('%d %b %Y')
                  # details for the movie
                  torrent_released[torrent_title] = [movie_desc, pub_date]
            

      return torrent_released


def display_notification(torrent_data):
      ''' This displays the notification in ubantu '''

      dir_path = os.path.dirname(os.path.realpath(__file__))

      # init the notifier
      notify.init("notifier")
      for name,desc in torrent_data.items():
            time.sleep(5)

            # get description and img path
            msg = str(desc[0]) +"\n"+desc[1]
            img_path = dir_path + "/img/" + name + "/cover.jpg"

            # notify the message
            n = notify.Notification(name, msg , img_path)
            n.show()

           




if __name__ == '__main__':
      torrents_data = invoke_feed()
      display_notification(torrents_data)


'''
INSTALLS :
----------------------------------------------
      sudo apt-get install python-setuptools
	sudo apt-get install python3-feedparser	
      sudo apt-get install python3-pip
'''