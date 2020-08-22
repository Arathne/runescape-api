from api import db, Items
import requests
import json
import math
import time

URI = "https://secure.runescape.com/m=itemdb_oldschool/"
SLEEP_INTERVAL = 60
MAX_CALLS = 24

# insert or replace
#
def insertItem( item ):
    try:
        query = Items.query.filter_by( id=item.id ).first()

        if query != None:
            db.session.delete(query)

        db.session.add( item )
        db.session.commit()
    except:
        print('failed to insert data')


# returns a list of available items
#
def getAvailableItems():
    url = '%sapi/catalogue/category.json?category=1' % URI
    try:
        response = requests.get(url)
        return response.json()['alpha']
    except:
        return []



# get 12 items on *page starting with letter *
#
def getItemPage( letter, page ):
    url = '%sapi/catalogue/items.json?category=1&alpha=%s&page=%s' % (URI, letter, page)
    try:
        response = requests.get(url)
        return response.json()['items']
    except:
        print('FAILED TO RETRIEVE PAGE')
        return []


# converts item array to object (makes it easier to insert to database)
#
def arrayToObject( array ):
    return Items(
        id=            array['id'],
        name=          array['name'],
        description=   array['description'],
        member=        array['members'],
        type_name=     array['type'],
        type_icon=     array['typeIcon'],
        icon=          array['icon'],
        icon_large=    array['icon_large'],
        current_price= array['current']['price'],
        current_trend= array['current']['trend'],
        today_price=   array['today']['price'],
        today_trend=   array['today']['trend'],
        day30_change=  '',
        day30_trend=   '',
        day90_change=  '',
        day90_trend=   '',
        day180_change= '',
        day180_trend=  ''
    )



# main script
#
if __name__ == "__main__":
    available = getAvailableItems()
    calls = 0

    for info in available:
        if info['letter'] != '#':
            total_pages = math.ceil(info['items']/12)
            for i in range(total_pages):
                if calls >= MAX_CALLS:
                    calls = 0
                    time.sleep( SLEEP_INTERVAL )
                
                pageNum = i+1
                itemList = getItemPage( info['letter'], pageNum )
                
                for item in itemList:
                    itemObj = arrayToObject(item)
                    insertItem( itemObj )
                
                calls += 1
                print( '%s : %s' % (info['letter'], pageNum) )
