import requests
from bs4 import BeautifulSoup
import pandas as pd

reviewlist = []


def get_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def get_reviews(soup):
    pass

for x in range(1,2):
    soup = get_soup(f'https://www.amazon.sg/Keychron-Hot-Swappable-Bluetooth-Mechanical-Compatible/dp/B08N44TC43/ref=asc_df_B08N44TC43/?tag=googleshoppin-22&linkCode=df0&hvadid=535373111890&hvpos=&hvnetw=g&hvrand=14585360175786125542&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9062543&hvtargid=pla-1793395535672&th=1')
    print(f'Getting page: {x}')
    print(soup)
    get_reviews(soup)
    print(len(reviewlist))
    """
    if not soup.find('li', {'class': 'a-disabled a-last'}):
        pass
    else:
        break
    """

"""
df = pd.DataFrame(reviewlist)
df.to_excel('sony-headphones.xlsx', index=False)
print('Fin.')
"""