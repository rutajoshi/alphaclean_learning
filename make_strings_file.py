
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

file_name = '/Users/Ruta/Desktop/Autolab/alphaclean/data_strings/all_table_strings.txt'
open(file_name, 'w').close() # Clear the file first
f = open(file_name, 'w')

all_strings = []
def write_data_strings(table):
    for tup in table:
        for val in tup:
            if type(val) is str and val not in all_strings:
                f.write(val + "\n")
                all_strings.append(val)

def main():
    write_data_strings(data)
    f.close()

if __name__ == "__main__":
    main()
