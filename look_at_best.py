__author__ = 'Eddie Pantridge'

import csv

import four_body_integrater
import draw

test_system_1 = [2.8291213371691626, 2.7812777033279894, 1.5888061867847556, 2.331376442114162,
               -5.881014435620725, -1.8493032992330949, -2.236597071307402, 10.193632294254009, 
			   -11.380648473295729, -5.026129324255478, -1.1512276780388004, -6.232053394492695,
			   -0.34665577463664254, 0.16478796531088702, 2.9954345865815624, 1.967348119152187, 
			   0.8570938897048066, 3.3231884238537197, 2.8043580416530998, 0.986520707713727]

test_system_2 = [2, 5, 3, 2,
				 0, 5, 0, -5, 
				 5, 0, -5, 0,
				 1, -3, -1, 0, 
				 0, -1, 0, 1]


def look_at_best_systems():
	rows = []
	with open('best_systems.csv', 'r') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			r = []
			for element in row:
				r.append(float(element))
			rows.append(r)
            
	csvfile.close()

	print ("Which system out of ", len(rows), " would you like to see.")

	system = rows[int(input("Enter number 0-" + str(len(rows)-1) + ": "))]
	print(len(system))
	print (system)
	e = four_body_integrater.get_estimates(system)
	draw.init_draw(e, system[:4])

	print ("Enter -1 next to exit")
	look_at_best_systems()

def loop_system (system):
    e = four_body_integrater.get_estimates(system)
    draw.init_draw(e, system[:4])
    loop_system(system)
	
#loop_system(test_system_2)
look_at_best_systems()
