import heterocl as hcl
#from Grid.GridProcessing import Grid
import numpy as np
import time
#from user_definer import *


####################################### USER-DEFINED VALUES ########################################


_bounds     = np.array([[-5.0, 5.0],[-5.0, 5.0],[-3.1415, 3.1415]])
_ptsEachDim = np.array([25, 25, 9])
_goal       = np.array([[2.5, 2.5], [1.5708, 2.3561]]) 

# set _actions based on ranges and number of steps
# format: range(lower bound, upper bound, number of steps)
vValues  = np.linspace(-2, 2, 9)
wValues  = np.linspace(-1, 1, 9)
_actions = []
for i in vValues:
    for j in wValues:
        _actions.append((i,j))
_actions = np.array(_actions)

_gamma    = np.array([0.93])
_epsilon  = np.array([.3])
_maxIters = np.array([5])
_trans    = np.zeros([1, 4]) # size: [maximum number of transition states available x 4]
_useNN    = np.array([1])



###################################### USER-DEFINED FUNCTIONS ######################################


# Given state and action, return successor states and their probabilities
# sVals: the coordinates of state
def transition(sVals, action, trans):
    trans[0, 0] = 1.0
    trans[0, 1] = sVals[0] + (0.6 * action[0] * hcl.tvm.intrin.cos(sVals[2]))
    trans[0, 2] = sVals[1] + (0.6 * action[0] * hcl.tvm.intrin.sin(sVals[2]))
    trans[0, 3] = sVals[2] + (0.6 * action[1])

    with hcl.if_(trans[0, 3] > 3.1415):
        trans[0, 3] = sVals[2] - 6.2832

    with hcl.elif_(trans[0, 3] < -3.1415):
        trans[0, 3] = sVals[2] + 6.2832

# Return the reward for taking action from state
def reward(sVals, action, trans, bounds, goal):
    rwd = hcl.scalar(0, "rwd")
    p   = hcl.scalar(0, "p")

    p[0]     = trans[0,0]
    sVals[0] = trans[0,1]
    sVals[1] = trans[0,2]
    sVals[2] = trans[0,3]


    # Check if out of bounds #######################################################################
    # TODO: Check if this is the correct approach

    with hcl.if_(hcl.or_(sVals[0] < bounds[0,0], sVals[0] > bounds[0,1], sVals[1] < bounds[1,0], sVals[1] > bounds[1,1])):
            rwd[0] = -400

    # Check if collision ###########################################################################
    # TODO

    # Check if goal state ##########################################################################
    
    with hcl.else_():
        dx  = hcl.scalar(0, "dx")
        dy  = hcl.scalar(0, "dy")
        mag = hcl.scalar(0, "mag")

        dx[0] = sVals[0] - goal[0,0]
        dy[0] = sVals[1] - goal[0,1]
        with hcl.if_(dx[0] < 0):
            dx[0] = goal[0,0] - sVals[0]
        with hcl.if_(dy[0] < 0):
            dy[0] = goal[0,1] - sVals[1]

        mag[0] = hcl.tvm.intrin.sqrt((dx[0] * dx[0]) + (dy[0] * dy[0]))

        with hcl.if_(hcl.and_(mag[0] <= 1, sVals[2] < goal[1,1], sVals[2] > goal[1,0])):
            rwd[0] = 1000

        # Else: standard move ######################################################################
        with hcl.else_():
            rwd[0] = 0
        return rwd[0]



######################################### HELPER FUNCTIONS #########################################


# Update the value function at position (i,j,k)
def updateQopt(i, j, k, a, iVals, sVals, Qopt, actions, intermeds, trans, interpols, gamma, bounds, goal, ptsEachDim, useNN):
    
    # set iVals equal to (i,j,k) and sVals equal to the corresponding state values at (i,j,k)
    updateStateVals(i, j, k, iVals, sVals, bounds, ptsEachDim)
    
    # call the transition function to obtain the outcome(s) of action a from state (si,sj,sk)
    transition(sVals, actions[a], trans)
    
    # initialize Qopt[i,j,k,a] with the immediate reward
    r             = hcl.scalar(0, "r")
    p             = hcl.scalar(0, "p")
    r[0]          = reward(sVals, actions[a], trans, bounds, goal)
    Qopt[i,j,k,a] = r[0]

    # maximize over successor Q-values
    with hcl.for_(0, trans.shape[0], name="si") as si:
        p[0]     = trans[si,0]
        sVals[0] = trans[si,1]
        sVals[1] = trans[si,2]
        sVals[2] = trans[si,3]

        #NOTE: nearest neighbour
        with hcl.if_(useNN[0] == 1):
            # obtain the nearest neighbour successor state
            stateToIndex(sVals, iVals, bounds, ptsEachDim)
            # maximize over successor state Q-values
            with hcl.if_(hcl.and_(iVals[0] < Qopt.shape[0], iVals[1] < Qopt.shape[1], iVals[2] < Qopt.shape[2])):
                with hcl.if_(hcl.and_(iVals[0] >= 0, iVals[1] >= 0, iVals[2] >= 0)):
                    with hcl.for_(0, actions.shape[0], name="a_") as a_:
                        with hcl.if_( (r[0] + (gamma[0] * (p[0] * Qopt[iVals[0],iVals[1],iVals[2],a_]))) > Qopt[i,j,k,a]):
                            # Takes into account the reward for taking an action
                            Qopt[i,j,k,a] = r[0] + (gamma[0] * (p[0] * Qopt[iVals[0],iVals[1],iVals[2],a_]))

                    r[0] += Qopt[i,j,k,a]

        # #NOTE: interpolation
        # with hcl.if_(useNN[0] == 0):
        #     # obtain linear interpolation weightings
        #     stateToIndexInterpolants(sVals, bounds, ptsEachDim, interpols)
        #     # maximize over successor state Q-values
        #     with hcl.for_(0, interpols.shape[0], name="ipl") as ipl:
        #         iplWeight = interpols[ipl, 0]
        #         iVals[0]  = interpols[ipl, 1]
        #         iVals[1]  = interpols[ipl, 2]
        #         iVals[2]  = interpols[ipl, 3]

        #         # if (ia, ij, ik) is within the state space, add its discounted value to action a
        #         with hcl.if_(hcl.and_(iVals[0] < Qopt.shape[0], iVals[1] < Qopt.shape[1], iVals[2] < Qopt.shape[2])):
        #             with hcl.if_(hcl.and_(iVals[0] >= 0, iVals[1] >= 0, iVals[2] >= 0)):
        #                 with hcl.for_(0, actions.shape[0], name="a_") as a_:
        #                     intermeds[a_] = (gamma[0] * iplWeight * (p * Qopt[iVals[0],iVals[1],iVals[2],a_]))
            
        #         # maximize over each possible action in intermeds to obtain the optimal value
        #         with hcl.for_(0, intermeds.shape[0], name="r_") as r_:
        #             with hcl.if_(Qopt[i,j,k,a] < r[0] + intermeds[r_]):
        #                 Qopt[i,j,k,a] = r[0] + intermeds[r_]
        #             intermeds[r_] = 0
        #         r[0] = Qopt[i,j,k,a]


# Returns 0 if convergence has been reached
def evaluateConvergence(newQ, oldQ, epsilon, reSweep):
    delta = hcl.scalar(0, "delta")
    # Calculate the difference, if it's negative, make it positive
    delta[0] = newQ[0] - oldQ[0]
    with hcl.if_(delta[0] < 0):
        delta[0] = delta[0] * -1
    with hcl.if_(delta[0] > epsilon[0]):
        reSweep[0] = 1


# convert state values into indeces using nearest neighbour
# NOTE: have to modify this to work with modular values
def stateToIndex(sVals, iVals, bounds, ptsEachDim):
    iVals[0] = (sVals[0] - bounds[0,0]) / ( (bounds[0,1] - bounds[0,0]) / (ptsEachDim[0]) )
    iVals[1] = (sVals[1] - bounds[1,0]) / ( (bounds[1,1] - bounds[1,0]) / (ptsEachDim[1]) )
    iVals[2] = (sVals[2] - bounds[2,0]) / ( (bounds[2,1] - bounds[2,0]) / (ptsEachDim[2]) )
    # NOTE: add 0.5 to simulate rounding
    iVals[0] = hcl.cast(hcl.Int(), iVals[0] + 0.5)
    iVals[1] = hcl.cast(hcl.Int(), iVals[1] + 0.5)
    iVals[2] = hcl.cast(hcl.Int(), iVals[2] + 0.5)


# convert indices into state values
def indexToState(iVals, sVals, bounds, ptsEachDim): 
    sVals[0] = (iVals[0] / ptsEachDim[0]) * (bounds[0,1] - bounds[0,0]) + bounds[0,0]
    sVals[1] = (iVals[1] / ptsEachDim[1]) * (bounds[1,1] - bounds[1,0]) + bounds[1,0]
    sVals[2] = (iVals[2] / ptsEachDim[2]) * (bounds[2,1] - bounds[2,0]) + bounds[2,0]


# set iVals equal to (i,j,k) and sVals equal to the corresponding state values at (i,j,k)
def updateStateVals(i, j, k, iVals, sVals, bounds, ptsEachDim):
    iVals[0] = i
    iVals[1] = j
    iVals[2] = k
    indexToState(iVals, sVals, bounds, ptsEachDim)


# given state values sVals, obtain the 8 possible successor states and their corresponding weight
def stateToIndexInterpolants(sVals, bounds, ptsEachDim, interpols):
    # obtain index values (not rounded)
    ia = (sVals[0] - bounds[0,0]) / ( (bounds[0,1] - bounds[0,0]) / ptsEachDim[0] )
    ja = (sVals[1] - bounds[1,0]) / ( (bounds[1,1] - bounds[1,0]) / ptsEachDim[1] )
    ka = (sVals[2] - bounds[2,0]) / ( (bounds[2,1] - bounds[2,0]) / ptsEachDim[2] )

    # obtain the 8 nearest states
    iMin = hcl.cast(hcl.Int(), ia)
    jMin = hcl.cast(hcl.Int(), ja)
    kMin = hcl.cast(hcl.Int(), ka)
    iMax = hcl.cast(hcl.Int(), ia + 1.0)
    jMax = hcl.cast(hcl.Int(), ja + 1.0)
    kMax = hcl.cast(hcl.Int(), ka + 1.0) 

    # assign values
    interpols[0, 1] = iMin
    interpols[0, 2] = jMin
    interpols[0, 3] = kMin

    interpols[1, 1] = iMax
    interpols[1, 2] = jMax
    interpols[1, 3] = kMax

    interpols[2, 1] = iMax
    interpols[2, 2] = jMin
    interpols[2, 3] = kMin

    interpols[3, 1] = iMin
    interpols[3, 2] = jMax
    interpols[3, 3] = kMin

    interpols[4, 1] = iMin
    interpols[4, 2] = jMin
    interpols[4, 3] = kMax

    interpols[5, 1] = iMax
    interpols[5, 2] = jMax
    interpols[5, 3] = kMin

    interpols[6, 1] = iMax
    interpols[6, 2] = jMin
    interpols[6, 3] = kMax

    interpols[7, 1] = iMin
    interpols[7, 2] = jMax
    interpols[7, 3] = kMax

    # set the weights of the 8 nearest states
    w1 = 1 - ( absdiff(ia, iMin) + absdiff(ja, jMin) + absdiff(ka, kMin) ) / 3  #w1 iMin, jMin, kMin
    w2 = 1 - ( absdiff(ia, iMax) + absdiff(ja, jMax) + absdiff(ka, kMax) ) / 3  #w2 iMax, jMax, kMax
    w3 = 1 - ( absdiff(ia, iMax) + absdiff(ja, jMin) + absdiff(ka, kMin) ) / 3  #w3 iMax, jMin, kMin
    w4 = 1 - ( absdiff(ia, iMin) + absdiff(ja, jMax) + absdiff(ka, kMin) ) / 3  #w4 iMin, jMax, kMin
    w5 = 1 - ( absdiff(ia, iMin) + absdiff(ja, jMin) + absdiff(ka, kMax) ) / 3  #w5 iMin, jMin, kMax
    w6 = 1 - ( absdiff(ia, iMax) + absdiff(ja, jMax) + absdiff(ka, kMin) ) / 3  #w6 iMax, jMax, kMin
    w7 = 1 - ( absdiff(ia, iMax) + absdiff(ja, jMin) + absdiff(ka, kMax) ) / 3  #w7 iMax, jMin, kMax
    w8 = 1 - ( absdiff(ia, iMin) + absdiff(ja, jMax) + absdiff(ka, kMax) ) / 3  #w8 iMin, jMax, kMax

    total = w1
    total += w2
    total += w3
    total += w4
    total += w5
    total += w6
    total += w7
    total += w8

    interpols[0, 0] = w1 / total
    interpols[1, 0] = w2 / total
    interpols[2, 0] = w3 / total
    interpols[3, 0] = w4 / total
    interpols[4, 0] = w5 / total
    interpols[5, 0] = w6 / total
    interpols[6, 0] = w7 / total
    interpols[7, 0] = w8 / total 


# TODO: move outside of this file
def absdiff(x, y):
    z = x - y
    with hcl.if_(z < 0):
        z = z * (-1)
    return z

######################################### VALUE ITERATION ##########################################


def value_iteration_3D():
    def solve_Qopt(Qopt, actions, intermeds, trans, interpols, gamma, epsilon, iVals, sVals, bounds, goal, ptsEachDim, count, maxIters, useNN):
            reSweep = hcl.scalar(1, "reSweep")
            oldQ    = hcl.scalar(0, "oldV")
            newQ    = hcl.scalar(0, "newV")
            with hcl.while_(hcl.and_(reSweep[0] == 1, count[0] < maxIters[0])):
                reSweep[0] = 0

                # Perform value iteration by sweeping in direction 1
                with hcl.Stage("Sweep_1"):
                    # For all states
                    with hcl.for_(0, Qopt.shape[0], name="i") as i:
                        with hcl.for_(0, Qopt.shape[1], name="j") as j:
                            with hcl.for_(0, Qopt.shape[2], name="k") as k:
                                # For all actions
                                with hcl.for_(0, Qopt.shape[3], name="a") as a:
                                    oldQ[0] = Qopt[i,j,k,a]
                                    updateQopt(i, j, k, a, iVals, sVals, Qopt, actions, intermeds, trans, interpols, gamma, bounds, goal, ptsEachDim, useNN)
                                    newQ[0] = Qopt[i,j,k,a]
                                    evaluateConvergence(newQ, oldQ, epsilon, reSweep)
                    count[0] += 1

                # # Perform value iteration by sweeping in direction 2
                # with hcl.Stage("Sweep_2"):
                #     # For all states
                #     with hcl.for_(1, Qopt.shape[0] + 1, name="i") as i:
                #         with hcl.for_(1, Qopt.shape[1] + 1, name="j") as j:
                #             with hcl.for_(1, Qopt.shape[2] + 1, name="k") as k:
                #                 i2 = Qopt.shape[0] - i
                #                 j2 = Qopt.shape[1] - j
                #                 k2 = Qopt.shape[2] - k

                #                 # For all actions
                #                 with hcl.for_(0, Qopt.shape[3], name="a") as a:
                #                     oldQ[0] = Qopt[i2,j2,k2,a]
                #                     updateQopt(i2, j2, k2, a, iVals, sVals, Qopt, actions, intermeds, trans, interpols, gamma, bounds, goal, ptsEachDim, useNN)
                #                     newQ[0] = Qopt[i2,j2,k2,a]
                #                     evaluateConvergence(newQ, oldQ, epsilon, reSweep)
                #     count[0] += 1

                # # Perform value iteration by sweeping in direction 3
                # with hcl.Stage("Sweep_3"):
                #     # For all states
                #     with hcl.for_(1, Qopt.shape[0] + 1, name="i") as i:
                #         with hcl.for_(0, Qopt.shape[1], name="j") as j:
                #             with hcl.for_(0, Qopt.shape[2], name="k") as k:
                #                 i2 = Qopt.shape[0] - i

                #                 # For all actions
                #                 with hcl.for_(0, Qopt.shape[3], name="a") as a:
                #                     oldQ[0] = Qopt[i2,j,k,a]
                #                     updateQopt(i2, j, k, a, iVals, sVals, Qopt, actions, intermeds, trans, interpols, gamma, bounds, goal, ptsEachDim, useNN)
                #                     newQ[0] = Qopt[i2,j,k,a]
                #                     evaluateConvergence(newQ, oldQ, epsilon, reSweep)
                #     count[0] += 1

                # # Perform value iteration by sweeping in direction 4
                # with hcl.Stage("Sweep_4"):
                #     # For all states
                #     with hcl.for_(0, Qopt.shape[0], name="i") as i:
                #         with hcl.for_(1, Qopt.shape[1] + 1, name="j") as j:
                #             with hcl.for_(0, Qopt.shape[2], name="k") as k:
                #                 j2 = Qopt.shape[0] - j

                #                 # For all actions
                #                 with hcl.for_(0, Qopt.shape[3], name="a") as a:
                #                     oldQ[0] = Qopt[i,j2,k,a]
                #                     updateQopt(i, j2, k, a, iVals, sVals, Qopt, actions, intermeds, trans, interpols, gamma, bounds, goal, ptsEachDim, useNN)
                #                     newQ[0] = Qopt[i,j2,k,a]
                #                     evaluateConvergence(newQ, oldQ, epsilon, reSweep)
                #     count[0] += 1

                # # Perform value iteration by sweeping in direction 5
                # with hcl.Stage("Sweep_5"):
                #     # For all states
                #     with hcl.for_(0, Qopt.shape[0], name="i") as i:
                #         with hcl.for_(0, Qopt.shape[1], name="j") as j:
                #             with hcl.for_(1, Qopt.shape[2] + 1, name="k") as k:
                #                 k2 = Qopt.shape[0] - k

                #                 # For all actions
                #                 with hcl.for_(0, Qopt.shape[3], name="a") as a:
                #                     oldQ[0] = Qopt[i,j,k2,a]
                #                     updateQopt(i, j, k2, a, iVals, sVals, Qopt, actions, intermeds, trans, interpols, gamma, bounds, goal, ptsEachDim, useNN)
                #                     newQ[0] = Qopt[i,j,k2,a]
                #                     evaluateConvergence(newQ, oldQ, epsilon, reSweep)
                #     count[0] += 1

                # # Perform value iteration by sweeping in direction 6
                # with hcl.Stage("Sweep_6"):
                #     # For all states
                #     with hcl.for_(1, Qopt.shape[0] + 1, name="i") as i:
                #         with hcl.for_(1, Qopt.shape[1] + 1, name="j") as j:
                #             with hcl.for_(0, Qopt.shape[2], name="k") as k:
                #                 i2 = Qopt.shape[0] - i
                #                 j2 = Qopt.shape[0] - j

                #                 # For all actions
                #                 with hcl.for_(0, Qopt.shape[3], name="a") as a:
                #                     oldQ[0] = Qopt[i2,j2,k,a]
                #                     updateQopt(i2, j2, k, a, iVals, sVals, Qopt, actions, intermeds, trans, interpols, gamma, bounds, goal, ptsEachDim, useNN)
                #                     newQ[0] = Qopt[i2,j2,k,a]
                #                     evaluateConvergence(newQ, oldQ, epsilon, reSweep)
                #     count[0] += 1

                # # Perform value iteration by sweeping in direction 7
                # with hcl.Stage("Sweep_7"):
                #     # For all states
                #     with hcl.for_(1, Qopt.shape[0] + 1, name="i") as i:
                #         with hcl.for_(0, Qopt.shape[1], name="j") as j:
                #             with hcl.for_(1, Qopt.shape[2] + 1, name="k") as k:
                #                 i2 = Qopt.shape[0] - i
                #                 k2 = Qopt.shape[0] - k

                #                 # For all actions
                #                 with hcl.for_(0, Qopt.shape[3], name="a") as a:
                #                     oldQ[0] = Qopt[i2,j,k2,a]
                #                     updateQopt(i2, j, k2, a, iVals, sVals, Qopt, actions, intermeds, trans, interpols, gamma, bounds, goal, ptsEachDim, useNN)
                #                     newQ[0] = Qopt[i2,j,k2,a]
                #                     evaluateConvergence(newQ, oldQ, epsilon, reSweep)
                #     count[0] += 1

                # # Perform value iteration by sweeping in direction 8
                # with hcl.Stage("Sweep_8"):
                #     # For all states
                #     with hcl.for_(0, Qopt.shape[0], name="i") as i:
                #         with hcl.for_(1, Qopt.shape[1] + 1, name="j") as j:
                #             with hcl.for_(1, Qopt.shape[2] + 1, name="k") as k:
                #                 j2 = Qopt.shape[0] - j
                #                 k2 = Qopt.shape[0] - k

                #                 # For all actions
                #                 with hcl.for_(0, Qopt.shape[3], name="a") as a:
                #                     oldQ[0] = Qopt[i,j2,k2,a]
                #                     updateQopt(i, j2, k2, a, iVals, sVals, Qopt, actions, intermeds, trans, interpols, gamma, bounds, goal, ptsEachDim, useNN)
                #                     newQ[0] = Qopt[i,j2,k2,a]
                #                     evaluateConvergence(newQ, oldQ, epsilon, reSweep)
                #     count[0] += 1


    ###################################### SETUP PLACEHOLDERS ######################################
    
    hcl.init()
    hcl.config.init_dtype = hcl.Float()

    # NOTE: trans is a tensor with size = maximum number of transitions
    # NOTE: intermeds must have size  [# possible actions]
    # NOTE: transition must have size [# possible outcomes, #state dimensions + 1]
    Qopt       = hcl.placeholder(tuple([25, 25, 9, 81]), name="Qopt", dtype=hcl.Float())
    gamma      = hcl.placeholder((0,), "gamma")
    count      = hcl.placeholder((0,), "count")
    epsilon    = hcl.placeholder((0,), "epsilon")
    actions    = hcl.placeholder(tuple(_actions.shape), name="actions", dtype=hcl.Float())
    intermeds  = hcl.placeholder(tuple([_actions.shape[0]]), name="intermeds", dtype=hcl.Float())
    trans      = hcl.placeholder(tuple(_trans.shape), name="successors", dtype=hcl.Float())
    bounds     = hcl.placeholder(tuple(_bounds.shape), name="bounds", dtype=hcl.Float())
    goal       = hcl.placeholder(tuple(_goal.shape), name="goal", dtype=hcl.Float())
    ptsEachDim = hcl.placeholder(tuple([3]), name="ptsEachDim", dtype=hcl.Float())
    sVals      = hcl.placeholder(tuple([3]), name="sVals", dtype=hcl.Float())
    iVals      = hcl.placeholder(tuple([3]), name="iVals", dtype=hcl.Float())
    maxIters   = hcl.placeholder((0,), "maxIters")

    # required for linear interpolation
    interpols  = hcl.placeholder(tuple([8, 4]), name="interpols", dtype=hcl.Float())
    useNN      = hcl.placeholder((0,), "useNN")

    # Create a static schedule -- graph
    s = hcl.create_schedule([Qopt, actions, intermeds, trans, interpols, gamma, epsilon, iVals, sVals, bounds, goal, ptsEachDim, count, maxIters, useNN], solve_Qopt)
    

    ########################################## INITIALIZE ##########################################

    # Convert the python array to hcl type array
    Q_opt      = hcl.asarray(np.zeros([25, 25, 9, 81]))
    intermeds  = hcl.asarray(np.ones(_actions.shape[0]))
    trans      = hcl.asarray(_trans)
    gamma      = hcl.asarray(_gamma)
    epsilon    = hcl.asarray(_epsilon)
    count      = hcl.asarray(np.zeros(1))
    actions    = hcl.asarray(_actions)
    bounds     = hcl.asarray(_bounds)
    goal       = hcl.asarray(_goal)
    ptsEachDim = hcl.asarray(_ptsEachDim)
    sVals      = hcl.asarray(np.zeros([3]))
    iVals      = hcl.asarray(np.zeros([3])) 
    maxIters   = hcl.asarray(_maxIters)

    # required for linear interpolation
    interpols  = hcl.asarray( np.zeros([8, 4]) )
    useNN      = hcl.asarray(_useNN)

    ######################################### PARALLELIZE ##########################################

    # s_1 = solve_Qopt.Sweep_1
    # s_2 = solve_Qopt.Sweep_2
    # s_3 = solve_Qopt.Sweep_3
    # s_4 = solve_Qopt.Sweep_4
    # s_5 = solve_Qopt.Sweep_5
    # s_6 = solve_Qopt.Sweep_6
    # s_7 = solve_Qopt.Sweep_7
    # s_8 = solve_Qopt.Sweep_8

    # s[s_1].parallel(s_1.i)
    # s[s_2].parallel(s_2.i)
    # s[s_3].parallel(s_3.i)
    # s[s_4].parallel(s_4.i)
    # s[s_5].parallel(s_5.i)
    # s[s_6].parallel(s_6.i)
    # s[s_7].parallel(s_7.i)
    # s[s_8].parallel(s_8.i)

    # Use this graph and build an executable
    f = hcl.build(s, target="llvm")


    ########################################### EXECUTE ############################################

    t_s = time.time()
    f(Q_opt, actions, intermeds, trans, interpols, gamma, epsilon, iVals, sVals, bounds, goal, ptsEachDim, count, maxIters, useNN)
    t_e = time.time()

    Q = Q_opt.asnumpy()
    c = count.asnumpy()

    print(Q)
    print()
    print("Finished in ", int(c[0]), " iterations")
    print("Took        ", t_e-t_s, " seconds")


# Test function
value_iteration_3D()
