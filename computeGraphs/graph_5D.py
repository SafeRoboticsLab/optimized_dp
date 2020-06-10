import heterocl as hcl
import numpy as np
import time
from computeGraphs.CustomGraphFunctions import *
from user_definer import *

##############################  5D DERIVATIVE FUNCTIONS #############################
def spa_derivX5_5d(i, j, k, l, m, V, g):  # Left -> right == Outer Most -> Inner Most
    left_deriv = hcl.scalar(0, "left_deriv")
    right_deriv = hcl.scalar(0, "right_deriv")
    if 5 not in g.pDim:
        with hcl.if_(m == 0):
            left_boundary = hcl.scalar(0, "left_boundary")
            left_boundary[0] = V[i, j, k, l, m] + my_abs(V[i, j, k, l, m + 1] - V[i, j, k, l, m]) * my_sign(
                V[i, j, k, l, m])
            left_deriv[0] = (V[i, j, k, l, m] - left_boundary[0]) / g.dx[4]
            right_deriv[0] = (V[i, j, k, l, m + 1] - V[i, j, k, l, m]) / g.dx[4]
        with hcl.elif_(m == V.shape[4] - 1):
            right_boundary = hcl.scalar(0, "right_boundary")
            right_boundary[0] = V[i, j, k, l, m] + my_abs(V[i, j, k, l, m] - V[i, j, k, l, m - 1]) * my_sign(
                V[i, j, k, l, m])
            left_deriv[0] = (V[i, j, k, l, m] - V[i, j, k, l, m - 1]) / g.dx[4]
            right_deriv[0] = (right_boundary[0] - V[i, j, k, l, m]) / g.dx[4]
        with hcl.elif_(m != 0 and m != V.shape[4] - 1):
            left_deriv[0] = (V[i, j, k, l, m] - V[i, j, k, l, m - 1]) / g.dx[4]
            right_deriv[0] = (V[i, j, k, l, m + 1] - V[i, j, k, l, m]) / g.dx[4]
        return left_deriv[0], right_deriv[0]
    else:
        with hcl.if_(m == 0):
            left_boundary = hcl.scalar(0, "left_boundary")
            left_boundary[0] = V[i, j, k, l, V.shape[4] - 1]
            left_deriv[0] = (V[i, j, k, l, m] - left_boundary[0]) / g.dx[4]
            right_deriv[0] = (V[i, j, k, l, m + 1] - V[i, j, k, l, m]) / g.dx[4]
        with hcl.elif_(m == V.shape[4] - 1):
            right_boundary = hcl.scalar(0, "right_boundary")
            right_boundary[0] = V[i, j, k, l, 0]
            left_deriv[0] = (V[i, j, k, l, m] - V[i, j, k, l, m - 1]) / g.dx[4]
            right_deriv[0] = (right_boundary[0] - V[i, j, k, l, m]) / g.dx[4]
        with hcl.elif_(m != 0 and m != V.shape[4] - 1):
            left_deriv[0] = (V[i, j, k, l, m] - V[i, j, k, l, m - 1]) / g.dx[4]
            right_deriv[0] = (V[i, j, k, l, m + 1] - V[i, j, k, l, m]) / g.dx[4]
        return left_deriv[0], right_deriv[0]


def spa_derivX4_5d(i, j, k, l, m, V, g):  # Left -> right == Outer Most -> Inner Most
    left_deriv = hcl.scalar(0, "left_deriv")
    right_deriv = hcl.scalar(0, "right_deriv")
    if 4 not in g.pDim:
        with hcl.if_(l == 0):
            left_boundary = hcl.scalar(0, "left_boundary")
            left_boundary[0] = V[i, j, k, l, m] + my_abs(V[i, j, k, l + 1, m] - V[i, j, k, l, m]) * my_sign(
                V[i, j, k, l, m])
            left_deriv[0] = (V[i, j, k, l, m] - left_boundary[0]) / g.dx[3]
            right_deriv[0] = (V[i, j, k, l + 1, m] - V[i, j, k, l, m]) / g.dx[3]
        with hcl.elif_(l == V.shape[3] - 1):
            right_boundary = hcl.scalar(0, "right_boundary")
            right_boundary[0] = V[i, j, k, l, m] + my_abs(V[i, j, k, l, m] - V[i, j, k, l - 1, m]) * my_sign(
                V[i, j, k, l, m])
            left_deriv[0] = (V[i, j, k, l, m] - V[i, j, k, l - 1, m]) / g.dx[3]
            right_deriv[0] = (right_boundary[0] - V[i, j, k, l, m]) / g.dx[3]
        with hcl.elif_(l != 0 and l != V.shape[3] - 1):
            left_deriv[0] = (V[i, j, k, l, m] - V[i, j, k, l - 1, m]) / g.dx[3]
            right_deriv[0] = (V[i, j, k, l + 1, m] - V[i, j, k, l, m]) / g.dx[3]
        return left_deriv[0], right_deriv[0]
    else:
        with hcl.if_(l == 0):
            left_boundary = hcl.scalar(0, "left_boundary")
            left_boundary[0] = V[i, j, k, V.shape[3] - 1, m]
            left_deriv[0] = (V[i, j, k, l, m] - left_boundary[0]) / g.dx[3]
            right_deriv[0] = (V[i, j, k, l + 1, m] - V[i, j, k, l, m]) / g.dx[3]
        with hcl.elif_(l == V.shape[3] - 1):
            right_boundary = hcl.scalar(0, "right_boundary")
            right_boundary[0] = V[i, j, k, 0, m]
            left_deriv[0] = (V[i, j, k, l, m] - V[i, j, k, l - 1, m]) / g.dx[3]
            right_deriv[0] = (right_boundary[0] - V[i, j, k, l, m]) / g.dx[3]
        with hcl.elif_(l != 0 and l != V.shape[3] - 1):
            left_deriv[0] = (V[i, j, k, l, m] - V[i, j, k, l - 1, m]) / g.dx[3]
            right_deriv[0] = (V[i, j, k, l + 1, m] - V[i, j, k, l, m]) / g.dx[3]
        return left_deriv[0], right_deriv[0]


def spa_derivX3_5d(i, j, k, l, m, V, g):  # Left -> right == Outer Most -> Inner Most
    left_deriv = hcl.scalar(0, "left_deriv")
    right_deriv = hcl.scalar(0, "right_deriv")
    if 3 not in g.pDim:
        with hcl.if_(k == 0):
            left_boundary = hcl.scalar(0, "left_boundary")
            left_boundary[0] = V[i, j, k, l, m] + my_abs(V[i, j, k + 1, l, m] - V[i, j, k, l, m]) * my_sign(
                V[i, j, k, l, m])
            left_deriv[0] = (V[i, j, k, l, m] - left_boundary[0]) / g.dx[2]
            right_deriv[0] = (V[i, j, k + 1, l, m] - V[i, j, k, l, m]) / g.dx[2]
        with hcl.elif_(k == V.shape[2] - 1):
            right_boundary = hcl.scalar(0, "right_boundary")
            right_boundary[0] = V[i, j, k, l, m] + my_abs(V[i, j, k, l, m] - V[i, j, k - 1, l, m]) * my_sign(
                V[i, j, k, l, m])
            left_deriv[0] = (V[i, j, k, l, m] - V[i, j, k - 1, l, m]) / g.dx[2]
            right_deriv[0] = (right_boundary[0] - V[i, j, k, l, m]) / g.dx[2]
        with hcl.elif_(k != 0 and k != V.shape[2] - 1):
            left_deriv[0] = (V[i, j, k, l, m] - V[i, j, k - 1, l, m]) / g.dx[2]
            right_deriv[0] = (V[i, j, k + 1, l, m] - V[i, j, k, l, m]) / g.dx[2]
        return left_deriv[0], right_deriv[0]
    else:
        with hcl.if_(k == 0):
            left_boundary = hcl.scalar(0, "left_boundary")
            left_boundary[0] = V[i, j, V.shape[2] - 1, l, m]
            left_deriv[0] = (V[i, j, k, l, m] - left_boundary[0]) / g.dx[2]
            right_deriv[0] = (V[i, j, k + 1, l, m] - V[i, j, k, l, m]) / g.dx[2]
        with hcl.elif_(k == V.shape[2] - 1):
            right_boundary = hcl.scalar(0, "right_boundary")
            right_boundary[0] = V[i, j, 0, l, m]
            left_deriv[0] = (V[i, j, k, l, m] - V[i, j, k - 1, l, m]) / g.dx[2]
            right_deriv[0] = (right_boundary[0] - V[i, j, k, l, m]) / g.dx[2]
        with hcl.elif_(k != 0 and k != V.shape[2] - 1):
            left_deriv[0] = (V[i, j, k, l, m] - V[i, j, k - 1, l, m]) / g.dx[2]
            right_deriv[0] = (V[i, j, k + 1, l, m] - V[i, j, k, l, m]) / g.dx[2]
        return left_deriv[0], right_deriv[0]


def spa_derivX2_5d(i, j, k, l, m, V, g):  # Left -> right == Outer Most -> Inner Most
    left_deriv = hcl.scalar(0, "left_deriv")
    right_deriv = hcl.scalar(0, "right_deriv")
    if 2 not in g.pDim:
        with hcl.if_(j == 0):
            left_boundary = hcl.scalar(0, "left_boundary")
            left_boundary[0] = V[i, j, k, l, m] + my_abs(V[i, j + 1, k, l, m] - V[i, j, k, l, m]) * my_sign(
                V[i, j, k, l, m])
            left_deriv[0] = (V[i, j, k, l, m] - left_boundary[0]) / g.dx[1]
            right_deriv[0] = (V[i, j + 1, k, l, m] - V[i, j, k, l, m]) / g.dx[1]
        with hcl.elif_(j == V.shape[1] - 1):
            right_boundary = hcl.scalar(0, "right_boundary")
            right_boundary[0] = V[i, j, k, l, m] + my_abs(V[i, j, k, l, m] - V[i, j - 1, k, l, m]) * my_sign(
                V[i, j, k, l, m])
            left_deriv[0] = (V[i, j, k, l, m] - V[i, j - 1, k, l, m]) / g.dx[1]
            right_deriv[0] = (right_boundary[0] - V[i, j, k, l, m]) / g.dx[1]
        with hcl.elif_(j != 0 and j != V.shape[1] - 1):
            left_deriv[0] = (V[i, j, k, l, m] - V[i, j - 1, k, l, m]) / g.dx[1]
            right_deriv[0] = (V[i, j + 1, k, l, m] - V[i, j, k, l, m]) / g.dx[1]
        return left_deriv[0], right_deriv[0]
    else:
        with hcl.if_(j == 0):
            left_boundary = hcl.scalar(0, "left_boundary")
            left_boundary[0] = V[i, V.shape[1] - 1, k, l, m]
            left_deriv[0] = (V[i, j, k, l, m] - left_boundary[0]) / g.dx[1]
            right_deriv[0] = (V[i, j + 1, k, l, m] - V[i, j, k, l, m]) / g.dx[1]
        with hcl.elif_(j == V.shape[1] - 1):
            right_boundary = hcl.scalar(0, "right_boundary")
            right_boundary[0] = V[i, 0, k, l, m]
            left_deriv[0] = (V[i, j, k, l, m] - V[i, j - 1, k, l, m]) / g.dx[1]
            right_deriv[0] = (right_boundary[0] - V[i, j, k, l, m]) / g.dx[1]
        with hcl.elif_(j != 0 and j != V.shape[1] - 1):
            left_deriv[0] = (V[i, j, k, l, m] - V[i, j - 1, k, l, m]) / g.dx[1]
            right_deriv[0] = (V[i, j + 1, k, l, m] - V[i, j, k, l, m]) / g.dx[1]
        return left_deriv[0], right_deriv[0]


def spa_derivX1_5d(i, j, k, l, m, V, g):  # Left -> right == Outer Most -> Inner Most
    left_deriv = hcl.scalar(0, "left_deriv")
    right_deriv = hcl.scalar(0, "right_deriv")
    if 1 not in g.pDim:
        with hcl.if_(i == 0):
            left_boundary = hcl.scalar(0, "left_boundary")
            left_boundary[0] = V[i, j, k, l, m] + my_abs(V[i + 1, j, k, l, m] - V[i, j, k, l, m]) * my_sign(
                V[i, j, k, l, m])
            left_deriv[0] = (V[i, j, k, l, m] - left_boundary[0]) / g.dx[0]
            right_deriv[0] = (V[i + 1, j, k, l, m] - V[i, j, k, l, m]) / g.dx[0]
        with hcl.elif_(i == V.shape[0] - 1):
            right_boundary = hcl.scalar(0, "right_boundary")
            right_boundary[0] = V[i, j, k, l, m] + my_abs(V[i, j, k, l, m] - V[i - 1, j, k, l, m]) * my_sign(
                V[i, j, k, l, m])
            left_deriv[0] = (V[i, j, k, l, m] - V[i - 1, j, k, l, m]) / g.dx[0]
            right_deriv[0] = (right_boundary[0] - V[i, j, k, l, m]) / g.dx[0]
        with hcl.elif_(i != 0 and i != V.shape[0] - 1):
            left_deriv[0] = (V[i, j, k, l, m] - V[i - 1, j, k, l, m]) / g.dx[0]
            right_deriv[0] = (V[i + 1, j, k, l, m] - V[i, j, k, l, m]) / g.dx[0]
        return left_deriv[0], right_deriv[0]
    else:
        with hcl.if_(i == 0):
            left_boundary = hcl.scalar(0, "left_boundary")
            left_boundary[0] = V[V.shape[0] - 1, j, k, l, m]
            left_deriv[0] = (V[i, j, k, l, m] - left_boundary[0]) / g.dx[0]
            right_deriv[0] = (V[i + 1, j, k, l, m] - V[i, j, k, l, m]) / g.dx[0]
        with hcl.elif_(i == V.shape[0] - 1):
            right_boundary = hcl.scalar(0, "right_boundary")
            right_boundary[0] = V[0, j, k, l, m]
            left_deriv[0] = (V[i, j, k, l, m] - V[i - 1, j, k, l, m]) / g.dx[0]
            right_deriv[0] = (right_boundary[0] - V[i, j, k, l, m]) / g.dx[0]
        with hcl.elif_(i != 0 and i != V.shape[0] - 1):
            left_deriv[0] = (V[i, j, k, l, m] - V[i - 1, j, k, l, m]) / g.dx[0]
            right_deriv[0] = (V[i + 1, j, k, l, m] - V[i, j, k, l, m]) / g.dx[0]
        return left_deriv[0], right_deriv[0]


########################## 5D graph definition ########################

# Note that t has 2 elements t1, t2
def graph_5D():
    V_f = hcl.placeholder(tuple(g.pts_each_dim), name="V_f", dtype=hcl.Float())
    V_init = hcl.placeholder(tuple(g.pts_each_dim), name="V_init", dtype=hcl.Float())
    # Initial target set _ value function at t = 0 ~~ inputed by user
    l0 = hcl.placeholder(tuple(g.pts_each_dim), name="l0", dtype=hcl.Float())
    # Constraint function ~~ input by user ( not time-variant for now)
    G = hcl.placeholder(tuple(g.pts_each_dim), name="G", dtype=hcl.Float())
    t = hcl.placeholder((2,), name="t", dtype=hcl.Float())

    # Positions vector
    x1 = hcl.placeholder((g.pts_each_dim[0],), name="x1", dtype=hcl.Float())
    x2 = hcl.placeholder((g.pts_each_dim[1],), name="x2", dtype=hcl.Float())
    x3 = hcl.placeholder((g.pts_each_dim[2],), name="x3", dtype=hcl.Float())
    x4 = hcl.placeholder((g.pts_each_dim[3],), name="x4", dtype=hcl.Float())
    x5 = hcl.placeholder((g.pts_each_dim[4],), name="x5", dtype=hcl.Float())

    def graph_create(V_new, V_init, x1, x2, x3, x4, x5, t, l0, G):
        # Specify intermediate tensors
        deriv_diff1 = hcl.compute(V_init.shape, lambda *x: 0, "deriv_diff1")
        deriv_diff2 = hcl.compute(V_init.shape, lambda *x: 0, "deriv_diff2")
        deriv_diff3 = hcl.compute(V_init.shape, lambda *x: 0, "deriv_diff3")
        deriv_diff4 = hcl.compute(V_init.shape, lambda *x: 0, "deriv_diff4")
        deriv_diff5 = hcl.compute(V_init.shape, lambda *x: 0, "deriv_diff5")

        # Maximum derivative for each dim
        max_deriv1 = hcl.scalar(-1e9, "max_deriv1")
        max_deriv2 = hcl.scalar(-1e9, "max_deriv2")
        max_deriv3 = hcl.scalar(-1e9, "max_deriv3")
        max_deriv4 = hcl.scalar(-1e9, "max_deriv4")
        max_deriv5 = hcl.scalar(-1e9, "max_deriv5")

        # Min derivative for each dim
        min_deriv1 = hcl.scalar(1e9, "min_deriv1")
        min_deriv2 = hcl.scalar(1e9, "min_deriv2")
        min_deriv3 = hcl.scalar(1e9, "min_deriv3")
        min_deriv4 = hcl.scalar(1e9, "min_deriv4")
        min_deriv5 = hcl.scalar(1e9, "min_deriv5")

        # These variables are used to dissipation calculation
        max_alpha1 = hcl.scalar(-1e9, "max_alpha1")
        max_alpha2 = hcl.scalar(-1e9, "max_alpha2")
        max_alpha3 = hcl.scalar(-1e9, "max_alpha3")
        max_alpha4 = hcl.scalar(-1e9, "max_alpha4")
        max_alpha5 = hcl.scalar(-1e9, "max_alpha5")

        def step_bound():  # Function to calculate time step
            stepBoundInv = hcl.scalar(0, "stepBoundInv")
            stepBound = hcl.scalar(0, "stepBound")
            stepBoundInv[0] = max_alpha1[0] / g.dx[0] + max_alpha2[0] / g.dx[1] + max_alpha3[0] / g.dx[2] + max_alpha4[
                0] / g.dx[3] \
                              + max_alpha5[0] / g.dx[4]

            stepBound[0] = 0.8 / stepBoundInv[0]
            with hcl.if_(stepBound > t[1] - t[0]):
                stepBound[0] = t[1] - t[0]

            # Update the lower time ranges
            t[0] = t[0] + stepBound[0]
            # t[0] = min_deriv2[0]
            return stepBound[0]

        # Comparison with the initial value function
        def maxVWithV0(i, j, k, l, m):  # Take the max
            with hcl.if_(V_new[i, j, k, l, m] < l0[i, j, k, l, m]):
                V_new[i, j, k, l, m] = l0[i, j, k, l, m]

        def minVWithV0(i, j, k, l, m):  # Take the max
            with hcl.if_(V_new[i, j, k, l, m] > l0[i, j, k, l, m]):
                V_new[i, j, k, l, m] = l0[i, j, k, l, m]

        # Comparison with the constraint function
        def maxVWithCStraint(i, j, k, l, m):
             with hcl.if_(V_new[i, j, k, l, m] < G[i, j, k, l, m]):
                 V_new[i, j, k, l, m] = G[i, j, k, l, m]

        def minVWithCStraint(i, j, k, l, m):
             with hcl.if_(V_new[i, j, k, l, m] > G[i, j, k, l, m]):
                 V_new[i, j, k, l, m] = G[i, j, k, l, m]

        # Comparison with the previous value function of previous time step
        def minVWithVInit(i, j, k, l, m):
            with hcl.if_(V_new[i, j, k, l, m] > V_init[i, j, k, l, m]):
                V_new[i, j, k, l, m] = V_init[i, j, k, l, m]

        def maxVWithVInit(i, j, k, l, m):
            with hcl.if_(V_new[i, j, k, l, m] < V_init[i, j, k, l, m]):
                V_new[i, j, k, l, m] = V_init[i, j, k, l, m]

        # Calculate Hamiltonian for every grid point in V_init
        with hcl.Stage("Hamiltonian"):
            with hcl.for_(0, V_init.shape[0], name="i") as i:
                with hcl.for_(0, V_init.shape[1], name="j") as j:
                    with hcl.for_(0, V_init.shape[2], name="k") as k:
                        with hcl.for_(0, V_init.shape[3], name="l") as l:
                            with hcl.for_(0, V_init.shape[4], name="m") as m:
                                    # Variables to calculate dV_dx
                                    dV_dx1_L = hcl.scalar(0, "dV_dx1_L")
                                    dV_dx1_R = hcl.scalar(0, "dV_dx1_R")
                                    dV_dx1 = hcl.scalar(0, "dV_dx1")
                                    dV_dx2_L = hcl.scalar(0, "dV_dx2_L")
                                    dV_dx2_R = hcl.scalar(0, "dV_dx2_R")
                                    dV_dx2 = hcl.scalar(0, "dV_dx2")
                                    dV_dx3_L = hcl.scalar(0, "dV_dx3_L")
                                    dV_dx3_R = hcl.scalar(0, "dV_dx3_R")
                                    dV_dx3 = hcl.scalar(0, "dV_dx3")
                                    dV_dx4_L = hcl.scalar(0, "dV_dx4_L")
                                    dV_dx4_R = hcl.scalar(0, "dV_dx4_R")
                                    dV_dx4 = hcl.scalar(0, "dV_dx4")
                                    dV_dx5_L = hcl.scalar(0, "dV_dx5_L")
                                    dV_dx5_R = hcl.scalar(0, "dV_dx5_R")
                                    dV_dx5 = hcl.scalar(0, "dV_dx5")

                                    # No tensor slice operation
                                    # dV_dx_L[0], dV_dx_R[0] = spa_derivX(i, j, k)
                                    dV_dx1_L[0], dV_dx1_R[0] = spa_derivX1_5d(i, j, k, l, m, V_init, g)
                                    dV_dx2_L[0], dV_dx2_R[0] = spa_derivX2_5d(i, j, k, l, m, V_init, g)
                                    dV_dx3_L[0], dV_dx3_R[0] = spa_derivX3_5d(i, j, k, l, m, V_init, g)
                                    dV_dx4_L[0], dV_dx4_R[0] = spa_derivX4_5d(i, j, k, l, m, V_init, g)
                                    dV_dx5_L[0], dV_dx5_R[0] = spa_derivX5_5d(i, j, k, l, m, V_init, g)

                                    # Saves spatial derivative diff into tables
                                    deriv_diff1[i, j, k, l, m] = dV_dx1_R[0] - dV_dx1_L[0]
                                    deriv_diff2[i, j, k, l, m] = dV_dx2_R[0] - dV_dx2_L[0]
                                    deriv_diff3[i, j, k, l, m] = dV_dx3_R[0] - dV_dx3_L[0]
                                    deriv_diff4[i, j, k, l, m] = dV_dx4_R[0] - dV_dx4_L[0]
                                    deriv_diff5[i, j, k, l, m] = dV_dx5_R[0] - dV_dx5_L[0]

                                    # Calculate average gradient
                                    dV_dx1[0] = (dV_dx1_L + dV_dx1_R) / 2
                                    dV_dx2[0] = (dV_dx2_L + dV_dx2_R) / 2
                                    dV_dx3[0] = (dV_dx3_L + dV_dx3_R) / 2
                                    dV_dx4[0] = (dV_dx4_L + dV_dx4_R) / 2
                                    dV_dx5[0] = (dV_dx5_L + dV_dx5_R) / 2

                                    # Find optimal control
                                    uOpt = my_object.opt_ctrl(t, (x1[i], x2[j], x3[k], x4[l], x5[m]), (
                                    dV_dx1[0], dV_dx2[0], dV_dx3[0], dV_dx4[0], dV_dx5[0]))
                                    # Find optimal disturbance
                                    dOpt = my_object.optDstb(t, (x1[i], x2[j], x3[k], x4[l], x5[m]),
                                        (dV_dx1[0], dV_dx2[0], dV_dx3[0], dV_dx4[0], dV_dx5[0]))

                                    # Find rates of changes based on dynamics equation
                                    dx1_dt, dx2_dt, dx3_dt, dx4_dt, dx5_dt = my_object.dynamics(t, (
                                    x1[i], x2[j], x3[k], x4[l], x5[m]), uOpt, dOpt)

                                    # Calculate Hamiltonian terms:
                                    V_new[i, j, k, l, m] = -(
                                                dx1_dt * dV_dx1[0] + dx2_dt * dV_dx2[0] + dx3_dt * dV_dx3[0] + dx4_dt *
                                                dV_dx4[0] + dx5_dt * dV_dx5[0])

                                    # Get derivMin
                                    with hcl.if_(dV_dx1_L[0] < min_deriv1[0]):
                                        min_deriv1[0] = dV_dx1_L[0]
                                    with hcl.if_(dV_dx1_R[0] < min_deriv1[0]):
                                        min_deriv1[0] = dV_dx1_R[0]

                                    with hcl.if_(dV_dx2_L[0] < min_deriv2[0]):
                                        min_deriv2[0] = dV_dx2_L[0]
                                    with hcl.if_(dV_dx2_R[0] < min_deriv2[0]):
                                        min_deriv2[0] = dV_dx2_R[0]

                                    with hcl.if_(dV_dx3_L[0] < min_deriv3[0]):
                                        min_deriv3[0] = dV_dx3_L[0]
                                    with hcl.if_(dV_dx3_R[0] < min_deriv3[0]):
                                        min_deriv3[0] = dV_dx3_R[0]

                                    with hcl.if_(dV_dx4_L[0] < min_deriv4[0]):
                                        min_deriv4[0] = dV_dx4_L[0]
                                    with hcl.if_(dV_dx4_R[0] < min_deriv4[0]):
                                        min_deriv4[0] = dV_dx4_R[0]

                                    with hcl.if_(dV_dx5_L[0] < min_deriv5[0]):
                                        min_deriv5[0] = dV_dx5_L[0]
                                    with hcl.if_(dV_dx5_R[0] < min_deriv5[0]):
                                        min_deriv5[0] = dV_dx5_R[0]

                                    # Get derivMax
                                    with hcl.if_(dV_dx1_L[0] > max_deriv1[0]):
                                        max_deriv1[0] = dV_dx1_L[0]
                                    with hcl.if_(dV_dx1_R[0] > max_deriv1[0]):
                                        max_deriv1[0] = dV_dx1_R[0]

                                    with hcl.if_(dV_dx2_L[0] > max_deriv2[0]):
                                        max_deriv2[0] = dV_dx2_L[0]
                                    with hcl.if_(dV_dx2_R[0] > max_deriv2[0]):
                                        max_deriv2[0] = dV_dx2_R[0]

                                    with hcl.if_(dV_dx3_L[0] > max_deriv3[0]):
                                        max_deriv3[0] = dV_dx3_L[0]
                                    with hcl.if_(dV_dx3_R[0] > max_deriv3[0]):
                                        max_deriv3[0] = dV_dx3_R[0]

                                    with hcl.if_(dV_dx4_L[0] > max_deriv4[0]):
                                        max_deriv4[0] = dV_dx4_L[0]
                                    with hcl.if_(dV_dx4_R[0] > max_deriv4[0]):
                                        max_deriv4[0] = dV_dx4_R[0]

                                    with hcl.if_(dV_dx5_L[0] > max_deriv5[0]):
                                        max_deriv5[0] = dV_dx5_L[0]
                                    with hcl.if_(dV_dx5_R[0] > max_deriv5[0]):
                                        max_deriv5[0] = dV_dx5_R[0]

        # Calculate dissipation amount
        with hcl.Stage("Dissipation"):
            uOptL1 = hcl.scalar(0, "uOptL1")
            uOptL2 = hcl.scalar(0, "uOptL2")
            uOptL3 = hcl.scalar(0, "uOptL3")
            uOptL4 = hcl.scalar(0, "uOptL4")
            uOptL5 = hcl.scalar(0, "uOptL5")

            uOptU1 = hcl.scalar(0, "uOptU1")
            uOptU2 = hcl.scalar(0, "uOptU2")
            uOptU3 = hcl.scalar(0, "uOptU3")
            uOptU4 = hcl.scalar(0, "uOptU4")
            uOptU5 = hcl.scalar(0, "uOptU5")

            dOptL1 = hcl.scalar(0, "dOptL1")
            dOptL2 = hcl.scalar(0, "dOptL2")
            dOptL3 = hcl.scalar(0, "dOptL3")
            dOptL4 = hcl.scalar(0, "dOptL4")
            dOptL5 = hcl.scalar(0, "dOptL5")

            dOptU1 = hcl.scalar(0, "dOptU1")
            dOptU2 = hcl.scalar(0, "dOptU2")
            dOptU3 = hcl.scalar(0, "dOptU3")
            dOptU4 = hcl.scalar(0, "dOptU4")
            dOptU5 = hcl.scalar(0, "dOptU5")

            # Storing alphas
            alpha1 = hcl.scalar(0, "alpha1")
            alpha2 = hcl.scalar(0, "alpha2")
            alpha3 = hcl.scalar(0, "alpha3")
            alpha4 = hcl.scalar(0, "alpha4")
            alpha5 = hcl.scalar(0, "alpha5")

            with hcl.for_(0, V_init.shape[0], name="i") as i:
                with hcl.for_(0, V_init.shape[1], name="j") as j:
                    with hcl.for_(0, V_init.shape[2], name="k") as k:
                        with hcl.for_(0, V_init.shape[3], name="l") as l:
                            with hcl.for_(0, V_init.shape[4], name="m") as m:
                                    dx_LL1 = hcl.scalar(0, "dx_LL1")
                                    dx_LL2 = hcl.scalar(0, "dx_LL2")
                                    dx_LL3 = hcl.scalar(0, "dx_LL3")
                                    dx_LL4 = hcl.scalar(0, "dx_LL4")
                                    dx_LL5 = hcl.scalar(0, "dx_LL5")

                                    dx_UL1 = hcl.scalar(0, "dx_UL1")
                                    dx_UL2 = hcl.scalar(0, "dx_UL2")
                                    dx_UL3 = hcl.scalar(0, "dx_UL3")
                                    dx_UL4 = hcl.scalar(0, "dx_UL4")
                                    dx_UL5 = hcl.scalar(0, "dx_UL5")
                                    #
                                    dx_LU1 = hcl.scalar(0, "dx_LU1")
                                    dx_LU2 = hcl.scalar(0, "dx_LU2")
                                    dx_LU3 = hcl.scalar(0, "dx_LU3")
                                    dx_LU4 = hcl.scalar(0, "dx_LU4")
                                    dx_LU5 = hcl.scalar(0, "dx_LU5")

                                    dx_UU1 = hcl.scalar(0, "dx_UU1")
                                    dx_UU2 = hcl.scalar(0, "dx_UU2")
                                    dx_UU3 = hcl.scalar(0, "dx_UU3")
                                    dx_UU4 = hcl.scalar(0, "dx_UU4")
                                    dx_UU5 = hcl.scalar(0, "dx_UU5")
                                    # Find LOWER BOUND optimal disturbance
                                    dOptL1[0], dOptL2[0], dOptL3[0], dOptL4[0], dOptL5[0] = my_object.optDstb(t, (x1[i], x2[j], x3[k], x4[l], x5[m]),
                                        (min_deriv1[0], min_deriv2[0], min_deriv3[0], min_deriv4[0], min_deriv5[0]))
                                    # Find UPPER BOUND optimal disturbance
                                    dOptU1[0], dOptU2[0], dOptU3[0], dOptU4[0], dOptU5[0] = my_object.optDstb(t, (x1[i], x2[j], x3[k], x4[l], x5[m]),
                                        (max_deriv1[0], max_deriv2[0], max_deriv3[0], max_deriv4[0], max_deriv5[0]))

                                    # Find LOWER BOUND optimal control
                                    uOptL1[0], uOptL2[0], uOptL3[0], uOptL4[0], uOptL5[0] = my_object.opt_ctrl(t, \
                                                                                    (x1[i], x2[j], x3[k], x4[l], x5[m]), (
                                                    min_deriv1[0], min_deriv2[0], min_deriv3[0], min_deriv4[0], min_deriv5[0],
                                    ))
                                    # Find UPPER BOUND optimal control
                                    uOptU1[0], uOptU2[0], uOptU3[0], uOptU4[0], uOptU5[0] = my_object.opt_ctrl(t, \
                                                                                    (x1[i], x2[j], x3[k], x4[l], x5[m]), (
                                                    max_deriv1[0], max_deriv2[0], max_deriv3[0], max_deriv4[0], max_deriv5[0],
                                    ))

                                    # Get upper bound and lower bound rates of changes
                                    dx_LL1[0], dx_LL2[0], dx_LL3[0], dx_LL4[0], dx_LL5[0] = my_object.dynamics(t, \
                                    (x1[i], x2[j], x3[k], x4[l], x5[m]), (uOptL1[0], uOptL2[0], uOptL3[0], uOptL4[0], uOptL5[0]),
                                                                        (dOptL1[0], dOptL2[0], dOptL3[0], dOptL4[0], dOptL5[0]))
                                    # Get absolute value of each
                                    dx_LL1[0] = my_abs(dx_LL1[0])
                                    dx_LL2[0] = my_abs(dx_LL2[0])
                                    dx_LL3[0] = my_abs(dx_LL3[0])
                                    dx_LL4[0] = my_abs(dx_LL4[0])
                                    dx_LL5[0] = my_abs(dx_LL5[0])

                                    dx_UL1[0], dx_UL2[0], dx_UL3[0], dx_UL4[0], dx_UL5[0] = my_object.dynamics(t, \
                                    (x1[i], x2[j], x3[k], x4[l], x5[m]), (uOptU1[0], uOptU2[0], uOptU3[0], uOptU4[0], uOptU5[0]),
                                                                (dOptL1[0], dOptL2[0], dOptL3[0], dOptL4[0], dOptL5[0]))
                                    # Get absolute value of each
                                    dx_UL1[0] = my_abs(dx_UL1[0])
                                    dx_UL2[0] = my_abs(dx_UL2[0])
                                    dx_UL3[0] = my_abs(dx_UL3[0])
                                    dx_UL4[0] = my_abs(dx_UL4[0])
                                    dx_UL5[0] = my_abs(dx_UL5[0])

                                    # Set maximum alphas
                                    alpha1[0] = my_max(dx_UL1[0], dx_LL1[0])
                                    alpha2[0] = my_max(dx_UL2[0], dx_LL2[0])
                                    alpha3[0] = my_max(dx_UL3[0], dx_LL3[0])
                                    alpha4[0] = my_max(dx_UL4[0], dx_LL4[0])
                                    alpha5[0] = my_max(dx_UL5[0], dx_LL5[0])

                                    dx_LU1[0], dx_LU2[0], dx_LU3[0], dx_LU4[0], dx_LU5[0] = my_object.dynamics(t, \
                                    (x1[i], x2[j], x3[k], x4[l], x5[m]), (uOptL1[0], uOptL2[0], uOptL3[0], uOptL4[0], uOptL5[0]),
                                    (dOptU1[0], dOptU2[0], dOptU3[0], dOptU4[0], dOptU5[0]))
                                    # Get absolute value of each
                                    dx_LU1[0] = my_abs(dx_LU1[0])
                                    dx_LU2[0] = my_abs(dx_LU2[0])
                                    dx_LU3[0] = my_abs(dx_LU3[0])
                                    dx_LU4[0] = my_abs(dx_LU4[0])
                                    dx_LU5[0] = my_abs(dx_LU5[0])

                                    alpha1[0] = my_max(alpha1[0], dx_LU1[0])
                                    alpha2[0] = my_max(alpha2[0], dx_LU2[0])
                                    alpha3[0] = my_max(alpha3[0], dx_LU3[0])
                                    alpha4[0] = my_max(alpha4[0], dx_LU4[0])
                                    alpha5[0] = my_max(alpha5[0], dx_LU5[0])

                                    dx_UU1[0], dx_UU2[0], dx_UU3[0], dx_UU4[0], dx_UU5[0] = my_object.dynamics(t, \
                                    (x1[i], x2[j], x3[k], x4[l], x5[m]), (uOptU1[0], uOptU2[0], uOptU3[0], uOptU4[0], uOptU5[0]),
                                    (dOptU1[0], dOptU2[0], dOptU3[0], dOptU4[0], dOptU5[0]))
                                    dx_UU1[0] = my_abs(dx_UU1[0])
                                    dx_UU2[0] = my_abs(dx_UU2[0])
                                    dx_UU3[0] = my_abs(dx_UU3[0])
                                    dx_UU4[0] = my_abs(dx_UU4[0])
                                    dx_UU5[0] = my_abs(dx_UU5[0])

                                    alpha1[0] = my_max(alpha1[0], dx_UU1[0])
                                    alpha2[0] = my_max(alpha2[0], dx_UU2[0])
                                    alpha3[0] = my_max(alpha3[0], dx_UU3[0])
                                    alpha4[0] = my_max(alpha4[0], dx_UU4[0])
                                    alpha5[0] = my_max(alpha5[0], dx_UU5[0])

                                    diss = hcl.scalar(0, "diss")
                                    diss[0] = 0.5 * (deriv_diff1[i, j, k, l, m] * alpha1[0] + deriv_diff2[
                                        i, j, k, l, m] * alpha2[0] \
                                                     + deriv_diff3[i, j, k, l, m] * alpha3[0] + deriv_diff4[
                                                         i, j, k, l, m] * alpha4[0] \
                                                     + deriv_diff5[i, j, k, l, m] * alpha5[0] )

                                    # Finally
                                    V_new[i, j, k, l, m] = -(V_new[i, j, k, l, m] - diss[0])
                                    # Get maximum alphas in each dimension

                                    # Calculate alphas
                                    with hcl.if_(alpha1 > max_alpha1):
                                        max_alpha1[0] = alpha1[0]
                                    with hcl.if_(alpha2 > max_alpha2):
                                        max_alpha2[0] = alpha2[0]
                                    with hcl.if_(alpha3 > max_alpha3):
                                        max_alpha3[0] = alpha3[0]
                                    with hcl.if_(alpha4 > max_alpha4):
                                        max_alpha4[0] = alpha4[0]
                                    with hcl.if_(alpha5 > max_alpha5):
                                        max_alpha5[0] = alpha5[0]

        # Determine time step
        delta_t = hcl.compute((1,), lambda x: step_bound(), name="delta_t")
        # hcl.update(t, lambda x: t[x] + delta_t[x])

        # Integrate
        # if compMethod == 'HJ_PDE':
        result = hcl.update(V_new,
                            lambda i, j, k, l, m: V_init[i, j, k, l, m] + V_new[i, j, k, l, m] * delta_t[0])
        if 'maxVWithV0' in compMethod:
            result = hcl.update(V_new, lambda i, j, k, l, m: maxVWithV0(i, j, k, l, m))
        if 'minVWithV0' in compMethod:
            result = hcl.update(V_new, lambda i, j, k, l, m: minVWithV0(i, j, k, l, m))
        if 'maxVWithVInit' in compMethod:
            result = hcl.update(V_new, lambda i, j, k, l, m: maxVWithVInit(i, j, k, l, m))
        if 'minVWithVInit' in compMethod:
            result = hcl.update(V_new, lambda i, j, k, l, m: minVWithVInit(i, j, k, l, m))
        if 'minVWithCStraint' in compMethod:
            result = hcl.update(V_new, lambda i, j, k, l, m: minVWithCStraint(i, j, k, l, m))
        if 'maxVWithCStraint' in compMethod:
            result = hcl.update(V_new, lambda i, j, k, l, m: maxVWithCStraint(i, j, k, l, m))
        # Copy V_new to V_init
        hcl.update(V_init, lambda i, j, k, l, m: V_new[i, j, k, l, m])
        return result


    s = hcl.create_schedule([V_f, V_init, x1, x2, x3, x4, x5, t, l0, G], graph_create)
    ##################### CODE OPTIMIZATION HERE ###########################
    print("Optimizing\n")

    # Accessing the hamiltonian and dissipation stage
    s_H = graph_create.Hamiltonian
    s_D = graph_create.Dissipation

    # Thread parallelize hamiltonian and dissipation
    s[s_H].parallel(s_H.i)
    s[s_D].parallel(s_D.i)

    # Inspect IR
    # if args.llvm:
    #    print(hcl.lower(s))

    # Return executable
    return (hcl.build(s))
