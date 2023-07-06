import requests
import re
import argparse
from lxml import etree

def parse_phone_number(s):
    if not (m := re.fullmatch(r'\+?[87]?(\d{10})', s)):
        raise Exception(f'Invalid phone number: {s}')
    return m[1]

def get_html_content(phone_number):
    url = f'https://кто-звонит.рф/{phone_number}/'
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text

def extract_info_chunk(tree, i):
    f = lambda s: tree.xpath(s)[0].rstrip(': ').rstrip('\n')
    k = f(f'//*[@id="onomere2"]/div[{i}]/span/text()')
    v = f(f'//*[@id="onomere2"]/div[{i}]/text()')
    return {k: v}

def extract_info(html):
    tree = etree.HTML(html)
    info = {}
    i = 0
    while True:
        i += 1
        try:
            chunk = extract_info_chunk(tree, i)
        except IndexError:
            return info
        info.update(chunk)

def print_info(phone_number, info):
    print(f'==== +7{phone_number} ====')
    for k, v in info.items():
        print(k, ': ', v, sep='')

def main():
    p = argparse.ArgumentParser()
    p.add_argument('phone_numbers', type=str, nargs='+')
    args = p.parse_args()
    for i in args.phone_numbers:
        phone_number = parse_phone_number(i)
        html_content = get_html_content(phone_number)
        info = extract_info(html_content)
        print_info(phone_number, info)
 
if __name__ == '__main__':
    main()