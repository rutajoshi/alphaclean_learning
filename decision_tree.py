from logic import *
from rule import Rule
from supervisor import acgreedy

from word_map_generator import *
from action_generator import *

from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
###############################################

#dataset
data = [('New Yorks',      'NY'),
        ('New York',       'NY'),
        ('San Francisco',  'SF'),
        ('San Francisco',  'SF'),
        ('San Jose',       'SJ'),
        ('New York',       'NY'),
        ('San Francisco',  'SFO'),
        ('Berkeley City',  'Bk'),
        ('San Mateo',      'SMO'),
        ('Albany',         'AB'),
        ('San Mateo',      'SM')]
action_gen = ActionGenerator(data)

def vectorize_pairs(states, actions):
    vectorized_states = []
    for state in states:
        print("Len of state = " + str(len(state)))
        vector_state = np.array(vectorize(state)).flatten()
        print("Shape of vector state = " + str(vector_state.shape))
        vectorized_states.append(vector_state)

    vectorized_actions = []
    action_gen.enumerate_actions()
    for action in actions:
        vector_action = np.array(action_gen.generate_1hot_action(action))
        print("Shape of vector action = " + str(vector_action.shape))
        vectorized_actions.append(vector_action)

    return np.array(vectorized_states), np.array(vectorized_actions)


#you need unique keys for all entries
d = {i : v for i,v in enumerate(data)}

#some property you want the db to satisfy
#E.g., one to one map between cities and codes
rule = Rule(lambda s,t: iff(eq(s,t,0), eq(s,t,1)))

# string trajectory, list of states, list of actions including DONE
trajectory, states, actions = acgreedy(rule, d)

# vectorize states and actions
states_v, actions_v = vectorize_pairs(states, actions)

X_train, y_train = states_v, actions_v
# X_train, X_test, y_train, y_test = train_test_split(states_v, actions_v, random_state=0)
estimator = DecisionTreeClassifier(max_leaf_nodes=3, random_state=0)
estimator.fit(X_train, y_train)

print("\n")
accuracy = 0
estimated_actions = []
for i in range(len(states_v)):
    state = states_v[i]
    action = actions_v[i]
    estimate = estimator.predict([state])
    if np.array_equal(estimate[0], action):
        accuracy += 1
    estimated_actions.append(action_gen.vector_to_action(estimate))
accuracy = accuracy / len(states_v) * 100
print("Accuracy = " + str(accuracy) + "%\n")

# Rollout estimated actions
