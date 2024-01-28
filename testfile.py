import random

import OMZ
import OPT_M
import OPT_pm
import cal_U
import creatData
import fixprice
import SoRP

"""1.creat data"""
needcreat = 0
usernum = 250
userd = 4
if needcreat:
    creatData.creatData(usernum)
    creatData.creatuserd(usernum, userd)
"""2.suffer user list"""
listnum = 100
users = creatData.creatuserlist(usernum, listnum)
"""3.run opt"""
optm = OPT_M.opt_m(userd, users)
"""4.run GD for Reward Price"""
"""read xij"""
with open("./xij.txt", 'r') as f_xij:
    xij_ = f_xij.readlines()
data_xij = []
for u in xij_:
    datas = []
    u = u.strip("\n")
    u = u.rstrip()
    data_split = u.split(" ")
    temp = list(data_split)
    for i in temp:
        p = int(i)
        datas.append(p)
    data_xij.append(datas)
SoRP.autoPrice(data_xij)
price = creatData.getPrice()
"""5.run opt_pm"""
opt_pm, ser_ut_opt, user_ut_opt, ser_pay_opt, winnum, coverrate_opt = OPT_pm.OPTpm(userd, users)
# start test
sever_uti_GDRP, user_uti_GDRP, sever_payment_GDRP, totalut_GDRP, winuser_GDRP, coverrate_GDRP = 0, 0, 0, 0, 0, 0
sever_uti_OMZ, user_uti_OMZ, sever_payment_OMZ, totalut_OMZ, winuser_OMZ, coverrate_OMZ = 0, 0, 0, 0, 0, 0
sever_uti_FIXPRICE, user_uti_FIXPRICE, sever_payment_FIXPRICE, totalut_FIXPRICE, winuser_FIXPRICE, coverrate_FIXPRICE = 0, 0, 0, 0, 0, 0
# sever_uti_OPTpm, user_uti_OPTpm, sever_payment_OPTpm, totalut_OPTpm, winuser_OPTpm = 0, 0, 0, 0, 0
rond = 10
for i in range(rond):
    print("round %d #####################################" % i)
    # suffer
    random.shuffle(users)
    # 1.GD for Reward Price test
    print("GDRP start.........................")
    sever_uti_GDRP0, user_uti_GDRP0, sever_payment_GDRP0, totalut_GDRP0, winuser_GDRP0, coverrate_GDRP0 = cal_U.calu(
        users, price, userd)
    sever_uti_GDRP += sever_uti_GDRP0
    user_uti_GDRP += user_uti_GDRP0
    sever_payment_GDRP += sever_payment_GDRP0
    totalut_GDRP += totalut_GDRP0
    winuser_GDRP += winuser_GDRP0
    coverrate_GDRP += coverrate_GDRP0
    print("GDRP end.........................")
    # 2.OMZ test
    print("OMZ start.........................")
    sever_uti_OMZ0, user_uti_OMZ0, sever_payment_OMZ0, totalut_OMZ0, winuser_OMZ0, coverrate_OMZ0 = OMZ.getOMZ(users,
                                                                                                               userd)
    sever_uti_OMZ += sever_uti_OMZ0
    user_uti_OMZ += user_uti_OMZ0
    sever_payment_OMZ += sever_payment_OMZ0
    totalut_OMZ += totalut_OMZ0
    winuser_OMZ += winuser_OMZ0
    coverrate_OMZ += coverrate_OMZ0
    print("OMZ end.........................")
    # 3.fix price test
    print("FIXPRICE start.........................")
    price_fix = fixprice.getprice()
    sever_uti_FIXPRICE0, user_uti_FIXPRICE0, sever_payment_FIXPRICE0, totalut_FIXPRICE0, winuser_FIXPRICE0, coverrate_FIXPRICE0 = cal_U.calu(
        users, price_fix, userd)
    sever_uti_FIXPRICE += sever_uti_FIXPRICE0
    user_uti_FIXPRICE += user_uti_FIXPRICE0
    sever_payment_FIXPRICE += sever_payment_FIXPRICE0
    totalut_FIXPRICE += totalut_FIXPRICE0
    winuser_FIXPRICE += winuser_FIXPRICE0
    coverrate_FIXPRICE += coverrate_FIXPRICE0
    print("FIXPRICE end.........................")
print("test end%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print("optm:", optm)
print("total utility:   OPT_pm:", round(opt_pm, 2), "    GDRP:", round(totalut_GDRP / rond, 2), "    OMZ:",
      round(totalut_OMZ / rond, 2), "   FIXPRICE:", round(totalut_FIXPRICE / rond, 2))
print("sever utility:   OPT_pm:", round(ser_ut_opt, 2), "   GDRP:", round(sever_uti_GDRP / rond, 2), "    OMZ:",
      round(sever_uti_OMZ / rond, 2), "    FIXPRICE:", round(sever_uti_FIXPRICE / rond, 2))
print("user utility:    OPT_pm:", round(user_ut_opt, 2), "    GDRP:", round(user_uti_GDRP / rond, 2), "   OMZ:",
      round(user_uti_OMZ / rond, 2), "  FIXPRICE:", round(user_uti_FIXPRICE / rond, 2))
print("sever payment:   OPT_pm:", round(ser_pay_opt, 2), "    GDRP:", round(sever_payment_GDRP / rond, 2), "  OMZ:",
      round(sever_payment_OMZ / rond, 2), " FIXPRICE:", round(sever_payment_FIXPRICE / rond, 2))
print("count of winners:    OPT_pm:", winnum, "   GDRP:", winuser_GDRP / rond, "  OMZ:", winuser_OMZ / rond,
      "    FIXPRICE:", winuser_FIXPRICE / rond)
print("POI coverage rate:    OPT_pm:", coverrate_opt, "   GDRP:", coverrate_GDRP / rond, "  OMZ:", coverrate_OMZ / rond,
      "    FIXPRICE:", coverrate_FIXPRICE / rond)
