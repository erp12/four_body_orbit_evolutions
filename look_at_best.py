__author__ = 'Eddie Pantridge'

import csv

import four_body_integrater
import draw

def look_at_best_systems():
    rows = []
    with open('best_systems.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        r = []
        for row in reader:
            for element in row:
                r.append(float(element))
            rows.append(r)
    csvfile.close()

    print "Which system out of ", len(rows), " would you like to see."

    system = rows[int(input("Enter number 1-" + str(len(rows))))]
    print system
    estimates = four_body_integrater.get_estimates(system)
    draw.init_draw(system[:4], estimates)

    print "Enter -1 next to exit"
    look_at_best_systems()

look_at_best_systems()