import cplex
import creatData
import numpy as np


def OPTpm(userd, userlist):
    pois = creatData.getPOI()
    userbid = creatData.getuserbid()
    price = creatData.getPrice()
    vm = pois[0]
    km = pois[1]
    d = float(userd)
    user_N = len(userlist)
    POI_M = len(vm)
    user_bid = [[] for i in range(user_N)]
    for i in range(user_N):
        user_bid[i] = userbid[userlist[i]]

    cpx = cplex.Cplex()
    cpx.objective.set_sense(cpx.objective.sense.maximize)
    var_x = [None for i in range(user_N)]

    for i in range(user_N):
        var_x[i] = list(cpx.variables.add(
            obj=[vm[j] - user_bid[i][j] for j in range(POI_M)],
            ub=[1] * POI_M,
            lb=[0] * POI_M,
            types=["I"] * POI_M,
            names=["x[%d]" % i + "[%c]" % str(j) for j in range(POI_M)]
        ))

    for m in range(POI_M):
        ind = [var_x[i][m] for i in range(user_N)]
        val = [1.0] * user_N
        cpx.linear_constraints.add(
            lin_expr=[cplex.SparsePair(ind=ind, val=val)],
            senses=["L"],
            rhs=[float(km[m])]
        )

    for i in range(user_N):
        ind = [var_x[i][m] for m in range(POI_M)]
        val = [1.0] * POI_M
        cpx.linear_constraints.add(
            lin_expr=[cplex.SparsePair(ind=ind, val=val)],
            senses=["L"],
            rhs=[d]
        )

    for i in range(user_N):
        for m in range(POI_M):
            ind = [var_x[i][m]]
            val = [1.0]
            cpx.linear_constraints.add(
                lin_expr=[cplex.SparsePair(ind=ind, val=val)],
                senses=["L"],
                rhs=[1.0]
            )

    for i in range(user_N):
        for m in range(POI_M):
            ind = [var_x[i][m]]
            val = [float(user_bid[i][m]) - price[m]]
            cpx.linear_constraints.add(
                lin_expr=[cplex.SparsePair(ind=ind, val=val)],
                senses=["L"],
                rhs=[0.0]
            )

    cpx.solve()
    print("Solution status =", cpx.solution.get_status_string())
    print("Optimal value:", cpx.solution.get_objective_value())
    cval = cpx.solution.get_objective_value()
    x_ij = cpx.solution.get_values("x[0][0]", "x[%d][%d]" % (user_N - 1, POI_M - 1))
    xij = np.array(x_ij)
    xij = xij.reshape(user_N, POI_M)
    print(xij)
    sever_ut = 0
    user_ut = 0
    sever_paid = 0
    winner = 0
    km_tmp = [0 for i in range(POI_M)]
    for i in range(len(userlist)):
        win_ = False
        for j in range(POI_M):
            if xij[i][j] == 1:
                sever_ut += round(vm[j] - price[j], 2)
                user_ut += round(price[j] - userbid[userlist[i]][j], 2)
                sever_paid += round(price[j], 2)
                win_ = True
                km_tmp[j] += 1
        if win_:
            winner += 1
    coverrate = sum(km_tmp) / sum(km)
    return cval, sever_ut, user_ut, sever_paid, winner, coverrate


