import copy
import random

import numpy as np

# Data
poi_nums = 6
poi_vm = [90, 70, 80, 80, 100, 70]
poi_d = [12, 10, 10, 12, 14, 10]

# Data Generated
def creatuserlist(usernum, listnum):
    users = [i for i in range(usernum)]
    userslist = np.random.choice(users, listnum, replace=False)
    random.shuffle(userslist)
    np.savetxt("userlist.txt", userslist, fmt="%d")
    return userslist


def creatuserd(usernums, userd):
    """creat d"""
    np.savetxt("user_can.txt", [], fmt="%d")
    user_can = []
    poi_inde = [i for i in range(poi_nums)]
    for j in range(usernums):
        sample = list(np.random.choice(poi_inde, random.randint(1, userd), replace=False))
        user_can.append(sample)
    print(user_can)
    with open('user_can.txt', 'a') as f1:
        for i in range(len(user_can)):
            np.savetxt(f1, user_can[i], delimiter=',', newline=' ', fmt='%d')
            f1.write('\n')
    f1.close()


def creatData(usernum):
    """ creat users"""
    user_bid = []
    user_bids = [[] for i in range(usernum)]
    for j in range(poi_nums):
        user_bid.append(np.random.normal(poi_vm[j] * 0.5, scale=5, size=usernum))
    for i in range(usernum):
        for j in range(poi_nums):
            user_bids[i].append(user_bid[j][i])
    np.savetxt("user_bid.txt", user_bids, fmt="%.4f")
    np.savetxt("poi.txt", [poi_vm, poi_d], fmt="%d")
    print("Datas created..........")
    return 0

# Data read
def getuserbid():
    with open("./user_bid.txt", 'r') as f_user:
        users_ = f_user.readlines()
    data_user = []
    for u in users_:
        datas = []
        u = u.strip("\n")
        u = u.rstrip()
        data_split = u.split(" ")
        temp = list(data_split)
        for i in temp:
            p = float(i)
            datas.append(p)
        data_user.append(datas)
    return data_user


def getPOI():
    with open("./poi.txt", 'r') as f_poi:
        pois_ = f_poi.readlines()
    data_poi = []
    for u in pois_:
        datas = []
        u = u.strip("\n")
        u = u.rstrip()
        data_split = u.split(" ")
        temp = list(data_split)
        for i in temp:
            p = int(i)
            datas.append(p)
        data_poi.append(datas)
    return data_poi


def getusercan():
    with open("./user_can.txt", 'r') as f_poiin:
        poiss_ = f_poiin.readlines()
    data_poiind = []
    for u in poiss_:
        datas = []
        u = u.strip("\n")
        u = u.rstrip()
        data_split = u.split(" ")
        temp = list(data_split)
        for i in temp:
            ua = int(i)
            datas.append(ua)
        data_poiind.append(datas)
    # print(data_poiind)
    return data_poiind


def getPrice():
    with open("./price.txt", 'r') as price:
        pi = price.readlines()
    data_p = []
    for p in pi:
        p = p.strip("\n")
        p = p.rstrip()
        data_p.append(float(p))
    return data_p


def getuserlist():
    with open("./userlist.txt", 'r') as userlist:
        userli = userlist.readlines()
    data_userlist = []
    for p in userli:
        p = p.strip("\n")
        p = p.rstrip()
        data_userlist.append(int(p))

    return data_userlist

