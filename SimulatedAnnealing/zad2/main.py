# Zadanie 2. Symulacja własnej fizyki. Dana jest siatka punktów w 2D (dla ambitnych: 3D) -
# reprezentacja np. w postaci mapy bitowej. Każdy punkt może być wypełniony lub nie.
# Zaproponuj funkcję energii (np. w oparciu o grawitację dodatkowo sterowaną kolorami -
# pełna dowolność - mile widziane rozwiązania kreatywne), a następnie dokonaj jej
# minimalizacji z wykorzystaniem SA. Przedstaw wizualizacje.

import numpy as np
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import random
import math


#kwadratowa mapa
class Map():
	def __init__(self):
		self.points = []
	def addPoint(self,p):
		self.points.append(p)
	def addPoints(self,points):
		for p in points:
			self.points.append(p)
	def findWholeEnergy(self):
		Energy = 0.0;
		for x in range(len(self.points)):
			for y in range(len(self.points) - x):
				if(x != (len(self.points) - 1 - y) ): 
					Energy = Energy + self.points[x].energy(self.points[len(self.points) - 1 - y])
		return Energy
	#end
	def printMe(self,p):
		fig = plt.figure()
		ax = fig.add_subplot(111,projection='3d')
		zData = []
		xData = []
		yData = []
		colorData = []	
		size = []
		#wartosci wspolrzednych dodane
		for i in self.points :
			zData.append(i.z)
			xData.append(i.x)
			yData.append(i.y)
			
			size.append(i.mass)
			
			colorData.append(i.colour)
		#end for
		ax.scatter(xData,yData,zData, c = colorData, marker = 'o', s = size)
		plt.savefig(p +'.png')
		plt.show()
		
	#end printing
	
	def annealing(self,temp,collingRate,iterations):
		energy = self.findWholeEnergy()
		for i in range(iterations):
			#losujemy punkt oraz jego nowe indeksy
			#nie dziala swap
			index , nx , ny, nz = random.randint(0,len(self.points) -1 ) , random.random() , random.random() , random.random()
			ox, oy, oz = self.points[index].x, self.points[index].y, self.points[index].z
			#print(1); print(self.points[index]); print("energia: "); print(energy)
			self.points[index].x, self.points[index].y, self.points[index].z = nx, ny, nz
			#print(2); print(self.points[index]);
			newEnergy = self.findWholeEnergy()
			#print(2); print(self.points[index]);print("Nowaenergia: "); print(newEnergy)
			if newEnergy < energy :
				energy = newEnergy
			elif newEnergy > energy : 
				delta = energy - newEnergy
				#wtedy przyjmujemy
				if (np.exp(delta/temp) > random.random() ):
					energy = newEnergy
				#odrzucamy
				else:
					energy = energy
					self.points[index].x, self.points[index].y, self.points[index].z = ox, oy, oz
			else:
				energy = energy
				self.points[index].x, self.points[index].y, self.points[index].z = ox, oy ,oz
			temp *= collingRate
		return energy	
	#end
	def complexoperation(self):
		self.printMe('before')
		energy = self.findWholeEnergy()
		print("Energia poczatkowego układu: "); print(energy);
		newEnergy = self.annealing(10000000,0.99,10000)
		print("Energia koncowego układu: "); print(newEnergy);
		self.printMe('after')
		print("Optymalizacja wyniosła: "); print(energy - newEnergy)
		return energy - newEnergy	
	#end
	
	
	
#end class

class Point():
	def __init__(self,a,b,z0,i,m,c):
		self.x = a
		self.y = b
		self.z = z0
		self.id = i
		self.mass = m 
		self.colour = c #char 'r' 'g' 'b' 'y'
	def __str__(self):
		return "(id:%d,x:%f,y:%f)" % (self.id,self.x,self.y)
	def __repr__(self):
		return "(id:%d,x:%f,y:%f)" % (self.id,self.x,self.y)
		
	#zwraca r^2
	def pathCost(p1,p2):
		return (p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2
	#end def
	#czy na pewno chce taka funkcje energi??
	def energy(self,point):
		if self.id != point.id:
			stala = self.colourConstant(point)
			path = self.pathCost(point)
			if path != 0:
				#print(xxxx)
				#print (stala*(self.mass*point.mass)/path)
				return (stala*(self.mass*point.mass)/path)
		return 0
	#end
	#ry rg rb gb gy by
	#xx -1
	#inne kombinacje nie wplywaja na siebie
	def colourConstant(self,point):
		stala = 0
		if self.colour == point.colour : # z tymi samymi kolorami maja sie odpychac jak ladunki
			stala = -1
		elif (self.colour == 'r' and point.colour == 'y') or (self.colour == 'y' and point.colour == 'r') :
			stala = -0.5
		elif (self.colour == 'r' and point.colour == 'g') or (self.colour == 'g' and point.colour == 'r') :
			stala = 0.5
		elif (self.colour == 'r' and point.colour == 'b') or (self.colour == 'b' and point.colour == 'r') :
			stala = 1
		elif (self.colour == 'g' and point.colour == 'b') or (self.colour == 'b' and point.colour == 'g') :
			stala = -0.5
		elif (self.colour == 'g' and point.colour == 'y') or (self.colour == 'y' and point.colour == 'g') :
			stala = -0.5
		elif (self.colour == 'b' and point.colour == 'y') or (self.colour == 'y' and point.colour == 'b') :
			stala = 0.5
		return stala
	#end	
#end class






if __name__ == "__main__":

#sensowna masa to tak pomiedzy 10 a 3000 zeby bylo wszystko ladnie widac
	points = []
	for i in range(9):
		points.append(Point(random.random(),random.random(),random.random(),i*4+1,250,'r'))
		points.append(Point(random.random(),random.random(),random.random(),i*4+2,100,'g'))
		points.append(Point(random.random(),random.random(),random.random(),i*4+3,200,'b'))
		points.append(Point(random.random(),random.random(),random.random(),i*4,150,'y'))
		
	map3d = Map()
	map3d.addPoints(points)

	map3d.complexoperation()
