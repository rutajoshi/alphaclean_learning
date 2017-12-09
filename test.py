from logic import *
from rule import Rule
from supervisor import acgreedy

#run alphaclean with gamma = 0
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

#you need unique keys for all entries
d = {i : v for i,v in enumerate(data)}

#some property you want the db to satisfy
#E.g., one to one map between cities and codes
rule = Rule(lambda s,t: iff(eq(s,t,0), eq(s,t,1)))

#get state-action list
print("\n")
print(acgreedy(rule, d)[0])

#E.g., all codes must be len 2
rule = Rule(lambda s: len(s[1]) == 2)
print("\n")
print(acgreedy(rule, d)[0])
print("\n")
