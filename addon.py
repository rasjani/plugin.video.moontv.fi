'''
   MoonTV.fi xbmc plugin
   ---------------------

   Watch programs from Finnish web tv MoonTV

   :copyright: (c) 2012 by Jani Mikkonen
   :license: GPLv3, see LICENSE.txt for more details.

'''

## Required imports
from xbmcswift2 import Plugin
from xbmcswift2 import download_page
from BeautifulSoup import BeautifulSoup as BS
from urlparse import urlparse
from urlparse import parse_qs

plugin = Plugin()

BASE_URL='http://moontv.fi/'
PROGRAMS_URL='http://moontv.fi/ohjelmat/'
BASE_URL_FMT='http://moontv.fi{0}'
PROGRAMS_URL_FMT='http://moontv.fi/ohjelmat{0}'

def _htmlify(url):
  return BS(download_page(url))

def _gen_item_from_episodepage(url):
  programhtml = _htmlify(url)

  episode_plot = programhtml.find('meta', { 'property':'og:description'})['content']
  episode_image = programhtml.find('meta', { 'property':'og:image'})['content']
  episode_title = programhtml.find('meta', { 'property':'og:title'})['content'].replace(" &raquo;",":")
  episode_url = parse_qs(urlparse(programhtml.find('meta', { 'property':'og:video'})['content']).query)['file'][0]
  return { 'label' : episode_title, 'thumbnail' : episode_image, 'path' : episode_url, 'is_playable' : True, 'info': { 'plot':episode_plot } }

@plugin.cached_route('/latestepisodes/')
def latestepisodes():
  items = []
  html = _htmlify(BASE_URL)
  latest = html.find('div',{ 'class' : 'thumbnails'} )
  episodes = latest.findAll('div')

  for episode in episodes:
      episodepage = episode.h6.a['href']
      item = _gen_item_from_episodepage(episodepage) 
      items.append(item)
 
  return items

@plugin.cached_route('/programs/')
def programs():
  items = []
  html = _htmlify(PROGRAMS_URL)
  programlist = html.find('ul', { 'id':'ohjelmat-list' } )
  programs = programlist.findAll('li')
  for program in programs:
    program_url = BASE_URL_FMT.format(program.a['href'])
    program_image = PROGRAMS_URL_FMT.format(program.img['src'])
    program_name = program.img['alt']
    program_desc = program.p.string
    items.append ( {
        'label' : program_name,
        'path'  : plugin.url_for('program', url = program_url ),
        'thumbnail' : program_image,
        'info': { 'plot':program_desc },
    })
    


  return items

@plugin.cached_route('/program/<url>/')
def program(url):
  items = []
  html = _htmlify(url)
  
  latest_ep_url = html.find('meta', { 'property':'og:url'})['content']
  item = _gen_item_from_episodepage(latest_ep_url)
  items.append(item)

  latest = html.find('div',{ 'class' : 'thumbnails'} )
  episodes = latest.findAll('div')

  for episode in episodes:
      episodepage = episode.h6.a['href']
      item = _gen_item_from_episodepage(episodepage)
      items.append(item)

  return items


@plugin.route('/')
def index():
    latest_episodes = {
        'label': plugin.get_string(30001),
        'path': plugin.url_for('latestepisodes')
    }
    programs = {
        'label': plugin.get_string(30002),
        'path': plugin.url_for('programs')
    }
    return [latest_episodes, programs]


if __name__ == '__main__':
    plugin.run()
