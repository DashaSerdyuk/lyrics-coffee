import requests
from bs4 import BeautifulSoup
import re
import os

def get_soup_by_artist(site, artist):
    base = site + artist[0] + '/' + artist
    site = requests.get(base)
    return BeautifulSoup(site.text, 'lxml'), base

def get_raw_lyrics(soup):
    songs_list = soup.find("div", {"id":"songs_nav"})
    s = str(list(songs_list)[9])
    found_songs = re.findall(r'(?<=<a href=")[^"]*', s)
    return found_songs

def parse_raw_lyrics(retrsongs, base):
    songs = {}
    for songname in retrsongs:
        songraw = requests.get(base + '/' + songname)
        parrallel_songs = BeautifulSoup(songraw.text, 'lxml').find("div", {"id": "click_area"})
        if parrallel_songs:
            lines = []
            for p in parrallel_songs.findAll("div", {"class": "original"}):
                lines.append(str(p.get_text()).replace('\n',''))
            songs[songname.replace('.html', '')] = lines
    return songs

def write_lyrics_to_file(artist, songs):
    newpath =  "lyrics/" + artist
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    i = 0
    for s in songs.keys():
        with open(newpath + '//' + artist + '_{0}.txt'.format(s), 'w', encoding='UTF-8') as ffff:
            for l in songs[s]:
                ffff.write(l + "\n")
        ffff.close()
        i += 1

        
artists = ['beyonce', 'taylor_swift', 'white_lies', 'destiny_s_child', 'imagine_dragons', 'borns', 'kaleo', 'foster_the_people', 'panic_at_the_disco', 'alt_j']
site = 'http://www.amalgama-lab.com/songs/'
for artist in artists:
    print("now handling: {0}... ".format(artist), end='')
    try:
        soup, base = get_soup_by_artist(site, artist)
        raw_lyrics = get_raw_lyrics(soup)
        lyrics_dict = parse_raw_lyrics(raw_lyrics, base)
        write_lyrics_to_file(artist, lyrics_dict)
        print('done.')
    except Exception as e:
        print('failed with {0}.'.format(e))

