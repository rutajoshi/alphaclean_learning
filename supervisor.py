"""
Module defines supervisors
"""
from cost import *

def acgreedy(rule, dataset, depth=10):
    c = CostEstimator([rule], dataset)

    state_action_list = []
    states = []
    actions = []

    for i in range(depth):
        rollout = sorted([(c.estimate(v), v) for v in rule._getNNFix(dataset)])
        top = rollout[0][0]

        state = c.currBest.copy()

        c.update(top[1],top[2])
        action = c.currMaps[-1]

        state_action_list.append({'state': state, 'action': action})

        # Store mapping from state to action as two lists
        states.append(state)
        actions.append(action)

        if top[0] == 0.0:
            break

    final_state = c.currBest.copy()
    state_action_list.append({'state': final_state, 'action': 'DONE'})

    return state_action_list, states, actions
