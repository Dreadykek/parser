import csv

if __name__ == '__main__':
    with open('output_test.csv', 'r') as file:
        r = csv.reader(file)
        object = {}
        for row in r:
            if any(sub in row[0] for sub in ['ranges', 'intensities']):
                temp = ','.join(row).replace('[', "").replace(']', "").split(':')
                if temp[0] == 'ranges':
                    object['ranges'] = temp[1].lstrip().split(', ')
                if temp[0] == 'intensities':
                    object['intensities'] = temp[1].lstrip().split(', ')
        print(object)