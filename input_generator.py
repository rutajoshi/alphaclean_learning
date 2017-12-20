import numpy as np

class InputGenerator:
    def __init__(self, table):
        self.table = table

    def generate(self):
        indices = np.random.choice(np.arange(len(self.table)), len(self.table), replace=True)
        new_table = []
        for i in indices:
            new_table.append(self.table[i])
        return new_table
