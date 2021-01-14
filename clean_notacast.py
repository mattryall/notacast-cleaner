#!/usr/bin/env python3

import os
import re
import sys
import urllib.request
from xml.etree import ElementTree
from xml.etree.ElementTree import Element


def get_feed(feed_url: str, namespaces: {str, str}) -> ElementTree:
    for prefix, uri in namespaces.items():
        ElementTree.register_namespace(prefix, uri)
    with urllib.request.urlopen(feed_url) as stream:
        return ElementTree.parse(stream)


def indent(elem: Element, level=0, spaces=2, last=False):
    """
    From ElementTree docs:
        <tag attrib>text<child/>...</tag>tail
    """

    def indent_str(indent_level):
        return "\n" + (" " * spaces * indent_level)

    if len(elem):  # has children
        if not elem.text or not elem.text.strip():
            # indent by (level + 1) before first child
            elem.text = indent_str(level + 1)
        for i, child in enumerate(elem):
            # each child indents its sibling by (level + 1), except the last
            last_child = (i == len(elem) - 1)
            indent(child, level + 1, spaces, last=last_child)

    if not elem.tail or not elem.tail.strip():
        # after an element, indent by (level) unless a last child, in which case (level - 1)
        elem.tail = indent_str(level - 1) if last else indent_str(level)
    return elem


def clean_feed():
    # url = 'https://www.patreon.com/rss/NotACastASOIAF?auth=' + os.environ['PATREON_TOKEN']
    url = 'file:///Users/mryall/src/asoiaf/notacast.rss'

    ns = {
        'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
        'atom': 'http://www.w3.org/2005/Atom',
        'googleplay': 'http://www.google.com/schemas/play-podcasts/1.0'
    }
    tree = get_feed(url, ns)

    root = tree.getroot()
    seen = {}
    for item in reversed(root.findall("channel/item")):
        title = item.findtext("title")
        if title in seen:
            root.find("channel").remove(item)
        else:
            seen[title] = True
    root.find("channel/title").text += " (Clean)"
    root.find("channel/atom:link", namespaces=ns).attrib['href'] = 'http://mattryall.net/asoiaf/notacast-clean.rss'

    indent(root)

    output = sys.stdout.buffer
    # output = 'notacast-pretty-stripped.rss'
    tree.write(output, encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    clean_feed()
