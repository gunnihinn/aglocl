#!/usr/bin/env python3

import re
import time
import sys
import requests
from bs4 import BeautifulSoup


def name_and_class(tag_name, class_name):
    return lambda e: e.name == tag_name and e.has_attr('class') and class_name in e['class']

def find_search_result_pages(url):
    'Return a list of URLs of the pages of search results'
    r = requests.get(url)
    if not r.status_code == 200:
        print('Could not get search results', file=sys.stderr)
        return None

    soup = BeautifulSoup(r.text, "html.parser")
    divs = soup.find_all(name_and_class('div', 'pagination'))
    if not divs:
        print("Didn't find any pages of search results",
            file=sys.stderr)
    div = divs[0]
    links = div.find_all('a')
    numbers = [link for link in links if re.match(r'^[0-9]+$', link.text)]
    last = numbers[-1]

    return [make_github_page_url(n) for n in range(1, int(last.text)+1)]

def make_github_page_url(number):
    url = ''.join([
        'https://github.com/search?',
        'p={n}'.format(n=number),
        '&q="curated+list"',
        '&type=Repositories',
        '&utf8=%E2%9C%93',
    ])
    return url

def find_repo_elements(soup):
    'Find repo <li> elements in GitHub search result soup'
    return soup.find_all(name_and_class('li', 'repo-list-item'))

def make_repo_dicts(repo_elements):
    'Make repo dictionaries out of repo <li> soups'
    dicts = [make_repo_dict(r) for r in repo_elements]
    return [d for d in dicts if d is not None]

def make_repo_dict(repo_element):
    'Make a repo dictionary out of a single repo <li> soup'
    # Find name and URL
    h3 = repo_element.find('h3')
    if not h3:
        print('No <h3> element found in <li> of search result',
            file=sys.stderr)
        return None

    a = h3.find('a')
    if not h3:
        print('No <a> element found in <li><h3> of search result',
            file=sys.stderr)
        return None

    name = a.text
    url = a['href']

    # Find description
    paras = repo_element.find_all(name_and_class('p', 'repo-list-description'))
    if not paras:
        print('No description <p> element found in <li> of search result',
            file=sys.stderr)
        return None
    p = paras[0]
    desc = p.text.strip()

    return {
        'name': name,
        'url': 'https://github.com{u}'.format(u=url),
        'description': desc,
    }

def repo_dicts_from_search(url):
    pages = find_search_result_pages(url)
    pages.reverse()

    reqs = []
    print('Got search result pages, making {0} requests...'
            .format(len(pages), file=sys.stderr))
    i = 0
    while pages:
        i += 1
        page = pages.pop()
        print('... making request {0}'.format(i), file=sys.stderr)
        while True:
            r = requests.get(page)
            if r.status_code == 200:
                reqs.append(r)
                time.sleep(5)
                break
            elif r.status_code == 429:
                print('GitHub server tired of us, waiting 60 seconds', file=sys.stderr)
                time.sleep(60)
            else:
                print('... request {0} FAILED: {1}'.format(i+1, r.status_code), file=sys.stderr)
                break

    print('Got search result requests, making soup...', file=sys.stderr)
    soups = [
        BeautifulSoup(r.text, "html.parser") for r in reqs 
        if r.status_code == 200
    ]
    print('Making repo elements...', file=sys.stderr)
    repo_elements = [find_repo_elements(soup) for soup in soups]
    repo_dicts = [make_repo_dicts(r) for r in repo_elements]

    dicts = []
    for rd in repo_dicts:
        dicts += rd

    return sorted(dicts, key=lambda d: d['name'])

def print_repo(dictionary):
    u = dictionary['url']
    n = dictionary['name']
    d = dictionary['description']
    return '* [{n}]({u}): {d}'.format(u=u, n=n, d=d)

if __name__ == '__main__':
    url = 'https://github.com/search?q=%22curated+list%22&type=Repositories&utf8=%E2%9C%93'
    repos = repo_dicts_from_search(url)

    lines = []
    with open('head.md') as head:
        lines = [line.strip() for line in head.readlines()]

    for repo in repos:
        lines.append(print_repo(repo))

    with open('README.md', 'w') as fh:
        for line in lines:
            print(line, file=fh)
