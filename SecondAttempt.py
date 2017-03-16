'''
Created on Aug 8, 2016
@author: el25453
'''


import json

#http://img.youtube.com/vi/<insert-youtube-video-id-here>/hqdefault.jpg

#inputThis = "search_query = " + inputThis
"""
print inputThis
result = requests.get("http://www.youtube.com/results?" + inputThis)
print result.text
with open("output.txt", "w") as thisFile:
    print >> thisFile, result.content
print "HEY",result.content.find("href=\"\/watch\?v=(.{11})")
#print("http://www.youtube.com/watch?v=" + result.content[0])
"""

import urllib
import urllib2
import os
import pprint
try:
    import requests
    from bs4 import BeautifulSoup
    from mutagen.mp3 import MP3
    from mutagen.easyid3 import EasyID3
    import mutagen.id3
    import eyed3
    from ID3 import *

    
except:
    os.system('pip install requests')
    os.system('pip install bs4')
    os.system('pip install lxml')
    os.system('pip install mutagen')
    os.system("pip install eyed3")
    os.system('pip install ID3')
    import eyed3
    import requests
    from mutagen.mp3 import MP3
    from mutagen.easyid3 import EasyID3
    import mutagen.id3
    from bs4 import BeautifulSoup


def searchThumbnail():
    inputThis = raw_input("Enter a youtube search query : ")
    #limited to once per minute it seems
    textToSearch = inputThis
    query = urllib.quote(textToSearch)
    print query
    #url = "https://www.youtube.com/results?search_query=" + query
    url = "https://www.youtube.com/results?q=" + query + "&sp=EgIQAQ%253D%253D"
    print url
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "lxml")
    imageString = ""
    #print soup
    print "look at next line"
    pprint.pprint(soup.findAll(attrs={'class':'yt-uix-tile-link'}))
    count = 0;
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        if count == 0:
            imageString = "http://img.youtube.com/vi/" + vid['href'].split("=")[1] + "/hqdefault.jpg"
            print 'https://www.youtube.com' + vid['href']
            print imageString
            urllib.urlretrieve(imageString, "test.jpg")
        count = count + 1

#http://www.programmableweb.com/news/how-to-query-youtube-through-its-python-apis/how-to/2014/03/26
def youtubeSearch(query):
    from apiclient.discovery import build
    from apiclient.errors import HttpError
    import logging
    logging.basicConfig()

    youtube = build("youtube", "v3", developerKey=API_KEY)
    
    response = youtube.search().list(
        q = query,
        part = "id,snippet",
        maxResults = 1,
    ).execute()
    
    transformResult = lambda response: {
        'id' : response['id']["videoId"],
        'title' : response['snippet']['title'],
        'thumbnail' : response['snippet']['thumbnails']['high'],
        'data' : response['snippet']['publishedAt']
        }
    
    thisFilter = lambda response : response['id']['kind'] == 'youtube#video'
    return map(transformResult, filter(thisFilter, response.get('items',[])))
    
#http://stackoverflow.com/questions/3207219/how-to-list-all-files-of-a-directory-in-python
def browseDialogue():
    import Tkinter
    import tkFileDialog
    import os
    
    root = Tkinter.Tk()
    root.withdraw() #use to hide tkinter window
    
    currdir = os.getcwd()
    tempdir = tkFileDialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
    if len(tempdir) > 0:
        print "You chose %s" % tempdir
    return tempdir
    
def filterFileName(thisString):
        stripped = (c for c in thisString if 0 < ord(c) < 127)
        improved = ''.join(stripped)
        improved = improved.replace(" \\xae ", "")
        last = improved.replace("," , " ")
        lastest = last.replace("&"," ")
        best = lastest.replace(":", "")
        bester = best.replace("-", " ")
        return bester
    
def searchDirectory():
    import urllib
    rootDirectory = browseDialogue()
    dirs = os.listdir( rootDirectory )
    #print rootDirectory
    # This would print all the files and directories
    mp3List = []
    for file in dirs:
        if file.split(".")[-1] == "mp3" :
            os.rename(os.path.join("",file),os.path.join("",filterFileName(file)))
            file = filterFileName(file)
            #print file
            thisList = youtubeSearch(file.split(".")[0])
            for item in thisList:
                print item['thumbnail']['url'], "-----", filterFileName(file.split(".mp3")[0] + ".jpg")
                #print "file:", file
                """
                id3info = ID3(file)
                id3info['ALBUM'] = file.split(".mp3")[0]
                id3info['ARTIST'] = "Youtube"
                """
                function=loadfile(file)
                print function
                function.tag.artist = u"Youtube"
                function.tag.album = file.split(".mp3")[0]
                urllib.urlretrieve(item['thumbnail']['url'], rootDirectory + "/" + filterFileName(file.split(".mp3")[0] + ".jpg"))
                imagedata = open(filterFileName(file.split(".mp3")[0] + ".jpg"),"rb").read()
                print "name of art", filterFileName(file.split(".mp3")[0] + ".jpg")
                print "imagedata", imagedata != None
                function.tag.images.set(3,imagedata,"image/jpeg")
                function.tag.save()
                
                """
                mp3file = MP3(rootDirectory + "/" + file, ID3 = EasyID3)
                try:
                    mp3file.add_tags(ID3=EasyID3)
                except mutagen.id3.error:
                    print("has tags")
                    
                urllib.urlretrieve(item['thumbnail']['url'], rootDirectory + "/" + filterFileName(file.split(".mp3")[0] + ".jpg"))

                print("file name:", file)
                print("/w root:", rootDirectory + "/" + file)
                #audiofile = eyed3.load(rootDirectory + "/" + file)
                audiofile = eyed3.load(file)
                audiofile.tag.artist = u"Youtube"
                audiofile.tag.album = file.split(".mp3")[0]
                print audiofile.tag.parse(file)
                #http://tuxpool.blogspot.com/2013/02/how-to-store-images-in-mp3-files-using.html
                imagedata = open(filterFileName(file.split(".mp3")[0] + ".jpg"),"rb").read()
                audiofile.tag.images.set(3,imagedata,"image/jpeg")
                audiofile.tag.save()
                print audiofile
                """
        else:
            #print file + " is not an mp3 file"
            pass
        
def loadfile(location):
      audiofile=eyed3.load(location)
      print "Opened {0} in EyeD3".format(location)
      return audiofile

if __name__ == "__main__":
    thisList = []
    with open ("apiKey.txt" , "r") as lines:
            for line in lines:
                line = line.replace("\n", "")
                thisList.append(line)
                API_KEY = str(thisList[0])
    print "API_KEY",API_KEY
    print ""
    searchDirectory()    
    
"""
#http://img.youtube.com/vi/<insert-youtube-video-id-here>/hqdefault.jpg
http://stackoverflow.com/questions/29069444/returning-the-urls-from-a-youtube-search
"""
