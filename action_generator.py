import numpy as np

class ActionGenerator:
    def __init__(self, table):
        assert len(table) > 0
        self.table = table
        self.total_actions = 0
        # maps (i,j) column pair to
        # (num_actions before the first action on those columns, num_actions on those columns)
        self.num_actions_map = {}
        self.actions_to_index = [[-1 for i in range(len(self.table[0]))] for j in range(len(self.table[0]))]
        self.sorted_col_sets = {} #maps column index i to sorted list of possible values

    def enumerate_actions(self):
        num_columns = len(self.table[0])
        table_array = np.array(self.table)
        for i in range(num_columns):
            self.sorted_col_sets[i] = list(sorted(set(table_array[:,i])))
            for j in range(num_columns):
                if i != j:
                    if i == 0:
                        self.sorted_col_sets[j] = list(sorted(set(table_array[:,j])))
                x_distinct = len(self.sorted_col_sets[i])
                y_distinct = len(self.sorted_col_sets[j])
                self.num_actions_map[(i,j)] = (self.total_actions, x_distinct*y_distinct)
                self.actions_to_index[i][j] = self.total_actions
                self.total_actions += x_distinct*y_distinct

    def generate_1hot_action(self, action):
        xi = action[0][0][0]
        x = action[0][0][1]
        yi = action[1]
        y = action[2]
        one_hot = np.zeros(self.total_actions)
        col_set_xi = self.sorted_col_sets[xi]
        col_set_yi = self.sorted_col_sets[yi]
        index = self.num_actions_map[(xi, yi)][0] + (len(col_set_xi) * col_set_xi.index(x)) + col_set_yi.index(y)
        one_hot[index] = 1
        return one_hot

    def vector_to_action(self, one_hot):
        index = np.where(one_hot==1)[0][0]
        xi, yi = 0, 0
        for i in range(len(self.table[0]))[::-1]:
            for j in range(len(self.table[0]))[::-1]:
                if self.actions_to_index[i][j] < index:
                    xi, yi = i, j
                    break
        index = index - self.num_actions_map[(xi, yi)][0]
        col_set_xi = self.sorted_col_sets[xi]
        col_set_yi = self.sorted_col_sets[yi]
        x_distinct = len(col_set_xi)
        y_distinct = len(col_set_yi)
        x_index = index // x_distinct
        y_index = index % x_distinct
        x = col_set_xi[x_index]
        y = col_set_yi[y_index]
        return (((xi, x),), yi, y)

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

def main():
    action_gen = ActionGenerator(data)
    action_gen.enumerate_actions()
    action = (((0, 'San Francisco'),), 1, 'SF')
    one_hot = action_gen.generate_1hot_action(action)
    print("\nAction: " + str(action))
    print("\nOne-Hot Vector: ")
    print(one_hot)
    action_retrieved = action_gen.vector_to_action(one_hot)
    print("\nRetrieved Action: " + str(action_retrieved))
    print("\n")


if __name__ == "__main__":
    main()
