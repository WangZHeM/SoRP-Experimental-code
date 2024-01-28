import cplex
import creatData
import numpy as np


def opt_m(userd, userlist):
    pois = creatData.getPOI()
    userbid = creatData.getuserbid()
    vm = pois[0]
    km = pois[1]
    d = float(userd)
    user_N = len(userlist)
    POI_M = len(vm)
    # Cplex
    cpx = cplex.Cplex()
    cpx.objective.set_sense(cpx.objective.sense.maximize)
    var_x = [None for i in range(user_N)]
    for i in range(user_N):
        var_x[i] = list(cpx.variables.add(
            obj=[vm[j] - userbid[userlist[i]][j] for j in range(POI_M)],
            ub=[1] * POI_M,
            lb=[0] * POI_M,
            types=["I"] * POI_M,
            names=["x[%d]" % i + "[%c]" % str(j) for j in range(POI_M)]))

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

    cpx.solve()
    print("Solution status =", cpx.solution.get_status_string())
    print("Optimal value:", cpx.solution.get_objective_value())
    cval = cpx.solution.get_objective_value()
    x_ij = cpx.solution.get_values("x[0][0]", "x[%d][%d]" % (user_N - 1, POI_M - 1))
    xij = np.array(x_ij)
    xij = xij.reshape(user_N, POI_M)
    print(xij)
    np.savetxt("xij.txt", xij, fmt="%d")
    return cval


