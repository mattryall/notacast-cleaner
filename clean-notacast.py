#!/usr/bin/env python3

from xml.etree import ElementTree

ns = {
    'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
    'atom': 'http://www.w3.org/2005/Atom',
    'googleplay': 'http://www.google.com/schemas/play-podcasts/1.0'
}
for prefix, uri in ns.items():
    ElementTree.register_namespace(prefix, uri)

tree = ElementTree.parse('/srv/www/mattryall.net/www/documents/asoiaf/notacast.rss')
root = tree.getroot()

seen = {}
for i in reversed(root.findall("channel/item")):
    title = i.findtext("title")
    if title in seen:
        root.find("channel").remove(i)
    else:
        seen[title] = True

root.find("channel/title").text += " (Clean)"
root.find("channel/atom:link", namespaces=ns).attrib['href'] = 'http://mattryall.net/asoiaf/notacast-clean.rss'

tree.write('/srv/www/mattryall.net/www/documents/asoiaf/notacast-clean.rss',
           encoding='utf-8',
           xml_declaration=True)

