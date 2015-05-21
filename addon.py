'''
   MoonTV.fi xbmc plugin
   ---------------------

   Watch programs from Finnish web tv MoonTV

   :copyright: (c) 2012 by Jani Mikkonen
   :license: GPLv3, see LICENSE.txt for more details.

'''

## Required imports
from xbmcswift2 import Plugin
from BeautifulSoup import BeautifulSoup as BS
from os.path import basename
from urlparse import urlparse
from urlparse import parse_qs


import urllib2

PLUGIN_NAME = 'MoonTV.fi'
PLUGIN_ID = 'plugin.video.moontv.fi'
plugin = Plugin(PLUGIN_NAME, PLUGIN_ID, __file__)



BASE_URL='http://moontv.fi/'
PROGRAMS_URL='http://www.moontv.fi/ohjelmat/'
BASE_URL_FMT='http://www.moontv.fi{0}'
PROGRAMS_URL_FMT='http://www.moontv.fi/ohjelmat{0}/'

# opener.addHeaders = [('User-agent', 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)')]
def _download_page(url):
  conn = None
  request = urllib2.Request(url)
  request.add_header('User-Agent', 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)')
  if plugin.get_setting('use_proxy',bool):
    proxies = {
      'http': 'http://' + plugin.get_setting('proxy_host',unicode) + ":" + plugin.get_setting('proxy_port', unicode),
      'https': 'http://' + plugin.get_setting('proxy_host', unicode) + ":" + plugin.get_setting('proxy_port', unicode),
    }
    opener = urllib2.build_opener(urllib2.ProxyHandler(proxies))
    urllib2.install_opener(opener)
    conn = opener.open(request)
  else:
    opener = urllib2.build_opener()
    urllib2.install_opener(opener)
    conn = opener.open(request)

  resp = conn.read()
  conn.close()
  return resp

def _htmlify(url):
  return BS(_download_page(url), convertEntities=BS.HTML_ENTITIES)

def _gen_item_from_episodepage(url):
  programhtml = _htmlify(url)
  sourceList = {}
  episode_image = programhtml.find('meta', { 'property':'og:image'})['content']
  episode_title = programhtml.find('meta', { 'property':'og:title'})['content'].replace(" &raquo;",":")
  episode_plot = programhtml.find('div', { 'class': 'span8'}).p.renderContents()

  tmp = programhtml.find('iframe')['src']
  tmp2 = _htmlify('http:' + tmp)
  sources = tmp2.findAll('source')
  for source in sources:
    sourceList[int(source['data-res'])] = source['src']

  maxRes = max(sourceList.keys())
  episode_url = sourceList[maxRes]

  return { 'label' : episode_title, 'thumbnail' : episode_image, 'path' : episode_url, 'is_playable' : True, 'info': { 'plot':episode_plot } }


@plugin.route('/latestepisodes/')
def latestepisodes():
  items = []
  html = _htmlify(BASE_URL)
  latest = html.find('div',{ 'class' : 'thumbnails'} )
  episodes = latest.findAll('div')

  for episode in episodes:
      episodepage = episode.h6.a['href']
      print episodepage
      #item = _gen_item_from_episodepage(episodepage)
      #items.append(item)

  return items

@plugin.route('/programs/')
def programs():
  items = []
  html = _htmlify(PROGRAMS_URL)
  programlist = html.find('div', { 'class': 'row ohjelmat'} )
  programs = programlist.findAll('div', { 'class': 'span2' })
  for program in programs:
    program_url = BASE_URL_FMT.format(program.a['href'])
    program_image = PROGRAMS_URL_FMT.format(program.img['src'])
    program_name = program.img['alt']
    print program_name
    print program_image
    print program_url

    items.append ( {
        'label' : program_name,
        'path'  : plugin.url_for('program', url = program_url ),
        'thumbnail' : program_image
    })

  return items

@plugin.route('/program/<url>/')
def program(url):
  items = []
  html = _htmlify(url)

  tmp = html.find('div', { 'class': 'row main thumbnails'})
  episodes = tmp.findAll('div', { 'class': 'span2 thumb loadThis' })

  for episode in episodes:
      episodepage = episode.h5.a['href']
      item = _gen_item_from_episodepage(episodepage)
      items.append(item)

  return items


@plugin.route('/')
def index():
    return [ { 'label': plugin.get_string(30001), 'path': plugin.url_for('latestepisodes') }, { 'label': plugin.get_string(30002), 'path': plugin.url_for('programs') } ]


if __name__ == '__main__':
    plugin.run()
