import numpy
import random
import math
import itertools
import time

class Point():
	def __init__(self,a,b,i):
		self.x = a
		self.y = b
		self.id = i
		#self.visited = False
	def __str__(self):
		return "(id:%d)" % (self.id)
	def __repr__(self):
		return "(id:%d)" % (self.id)
#end class

def pathCost(p1,p2):
	cost = (p1.x - p2.x)**2 + (p1.y - p2.y)**2
	return math.sqrt(cost)
#end def

#points to kolejnosc wierzcholkow w jakiej przechodzimy
def findWholeCost(points):
	cost = 0.0
	for x in range(len(points) - 1):
		cost += pathCost(points[x],points[x+1])
	#end for
	return cost
#end def

def findNewWay(points):
	newPoints = []
	for x in points:
		newPoints.insert( random.randint(0,len(newPoints)) , x ) 
	#end for
	return newPoints
#end def 

#zamieniamy tylko 2 punkty miejscami
def findSimilarWay(points):
	index = random.randint(0,len(points)-2)
	#zamieniamy index z index + 1
	points[index],points[index+1] = points[index + 1],points[index]
	return points
#end def

#trash
def findSemiOptimum(iterations,points):
	minimalCost = findWholeCost(points)
	for i in range(iterations):
		points = findNewWay(points)
		tmpCost = findWholeCost(points)
		if tmpCost < minimalCost : 
			minimalCost = tmpCost
		#end if
	#end for
	return (points,minimalCost)
#end def


#http://iswiki.if.uj.edu.pl/iswiki/images/2/20/AiSD_22._Symulowane_wy%C5%BCarzanie_%28problem_komiwoja%C5%BCera%29.pdf?fbclid=IwAR3ydX_0bF57HssMDLamxDXg_1OYVCNOUxn1xkA2e5aySDXRg9hzoept1ck	
#zmienione ze stalego procentowegox
def annealing(points,temp,collingRate,iterations):
	cost = findWholeCost(points)
	for i in range(iterations) :
		#losujemy index do zamiany
		simmilarWay = findSimilarWay(points)
		similarCost = findWholeCost(simmilarWay)
		#teraz jezeli kosz jest mniejszy to zamieniamy
		if similarCost < cost :
			cost = similarCost
			points = simmilarWay
		#jezeli koszt jest wiekszy to zmieniamy z jakims prawdopodobienstwem zaleznym od roznicy i temperatury
		else :
			delta =  cost - similarCost #ujemne
			if ( numpy.exp(delta/temp) > random.random() ):
				cost = similarCost
				points = simmilarWay
		temp *= collingRate
	return (points,cost)
#end def


def exactMinimalCost(points):
	minimalCost = 99999999999999.0;
	optimumList = []
	for x in itertools.permutations(points,len(points)):
		listX = list(x)
		tmpCost = findWholeCost(listX);
		if tmpCost < minimalCost:
			minimalCost = tmpCost
			optimumList = list(x)
		#end if
	#end for
	return (optimumList,minimalCost)
#end def


if __name__ == "__main__":
	points = []
	for i in range(10):
		points.append(Point(random.random(),random.random(),i))
		
	nSTime = time.time()
	(seq,cost) = annealing(points,10000000,0.99,10000)
	nETime = time.time()
	oSTime = time.time()
	(seq2,cost2) = exactMinimalCost(points)
	oETime = time.time()
	
	print("#########skrocony######")
	print(seq)
	print(cost)
	print( ("czas %f") % (nETime-nSTime))
	print("#########calosciowy######")
	print(seq2)
	print(cost2)
	print( ("czas %f") % (oETime-oSTime))
