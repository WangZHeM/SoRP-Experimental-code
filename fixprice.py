import math

import creatData

# Fix price
def getprice():
    pois = creatData.getPOI()
    vm = pois[0]
    price = []
    for vs in vm:
        price.append(vs * 0.4)
    return price

