import requests
from lxml import etree as et

url = "https://www.nbkr.kg/XML/daily.xml"


def get_quote(currency):
    try:
        quotes = requests.get(url)
    except Exception as e:
        print(e)
        return False
    if quotes.status_code == 200:
        root = et.fromstring(quotes.text.encode('utf-8'))
        for i in root:
            if i.attrib['ISOCode'] == currency:
                for x in i:
                    if x.tag == 'Value':
                        return {'response': True, 'price': x.text}
    else:
        return {'response': False, 'price': None}
