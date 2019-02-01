import random
import numpy
import time

class Point():
	def __init__(self,v,ifStatic):
		self.value = v
		self.static = ifStatic
	#end init
	def getVal(self):
		return self.value
	def getStatic(self):
		return self.static
	def canSwap(self,point2):
		return (self.static == point2.static == False)
	def setVal(self,val):
		self.value = val
#end class

#plansza sklada sie z listy wierszy
class Sudoku():
	def __init__(self):
		#bo wybieramy wiersz na osi pionowej
		self.row = []
		for i in range(9):
			tmplist = []
			for j in range(9):
				tmplist.append(Point(0,False))
			self.row.append(tmplist)
		#zainicjalizowana samymi -1
	#end init
	def setStaticPoint(self,v,h,value):
		self.row[v][h] = Point(value,True)
	#end def
	def swapPoints(self,v1,h1,v2,h2):
		if self.row[v2][h2].canSwap(self.row[v1][h1]):
			self.row[v1][h1], self.row[v2][h2] = self.row[v2][h2], self.row[v1][h1]
		else:
			print("Couldnot swap these points\n")
	#end def
	def printSudoku(self):#it is nice when digit has no sign
		line = "+-+-+-+-+-+-+-+-+-+"
		#drukujemy kazdy wiersz
		for v in range(9):
			line2 = "|" 
			for h in range(9):
				line2 += str( self.row[v][h].getVal() )
				line2 += "|"
			print(line)
			print(line2)
		print(line)
	#end def
	
	#no longer used
	#[2,3,4,....]
	#oznacza ze 1 uzylismy 2 razy, 2 uzylismy 3, 3 uzylismy 4 ...
	def timesUsed(self):
		used = []
		for i in range(9):
			used.append(0)
		#kazde uzylismy raz
		#teraz zliczamy
		for r in range(9):
			for k in range(9):
				if self.row[r][k].getVal() != 0:
					used[self.row[r][k].getVal() - 1] += 1
		return used
	#end def
	
	#no longer used there is 2.0 function
	#wypelniamy sudoku wszystkimi potrzebnymi cyferkami
	def fillSudoku(self):
		rowAndColumn = 0
		#potrzebujemy wiedziec ile czego mozemy uzyc na razie zakladamy ze kazdego po 
		used = self.timesUsed()
		print(used)
		#lecimy po calym used
		for i in range(9):
			while(used[i] != 9):
				#jesli pole jest nieustawione oraz jest niestatyczne
				if(self.row[rowAndColumn//9][rowAndColumn%9].getStatic() == False and self.row[rowAndColumn//9][rowAndColumn%9].getVal() == 0 ):
					self.row[rowAndColumn//9][rowAndColumn%9].setVal(i+1)
					used[i] += 1
				rowAndColumn += 1
			#end while
		#end for
	#end def
	
	def put(self,row,number):
		# print("xD")
		# print(row)
		# print(number)
		for col in range(9):
			if self.row[row][col].value == number :
				#print("xD")
				return
		
		for col in range(9):
			if self.row[row][col].value == 0 :
				self.row[row][col].value = number
				#print("Wstawiam");print(number);
				return
	
	#end def
	
	def fillSudoku2(self):
		for row in range(9):
			for number in range(9):
				#print(row);print(number+1);
				self.put(row,number+1)
	#end def
		
	
	def calculatePartiallScore(self,r,k):
		score = 0
		val = self.row[r][k].getVal()
		#liczymy w wierszu
		for i in range(9):
			#jesli to nie ta sama komorka oraz jesli to ta sama wartosc to dodajemy
			if i != k and self.row[r][i].getVal() == val:
				score += 1		
		#liczymy w kolumnie
		for i in range(9):
			#jesli to nie ta sama komorka oraz jesli to ta sama wartosc to dodajemy
			if i != r and self.row[i][k].getVal() == val:
				score += 1		
		return score
	#end def
	
	#najlepsze sudoku to takie ze score rownym 0
	# 0 oznacza ze nie bylo zadnych duplikatoww wierszu i kolumnie
	def calculateScore(self):
		score = 0
		for i in range(81):
			score += self.calculatePartiallScore(i//9,i%9)
		#end for
		return score
	#end def
	
	def setFirst(self):
		self.setStaticPoint(0,1,1)
		self.setStaticPoint(0,3,6)
		self.setStaticPoint(0,5,4)
		self.setStaticPoint(0,6,3)
		self.setStaticPoint(0,8,7)
		
		self.setStaticPoint(1,0,3)
		self.setStaticPoint(1,1,5)
		self.setStaticPoint(1,2,6)
		
		self.setStaticPoint(2,4,5)
		self.setStaticPoint(2,5,3)
		self.setStaticPoint(2,6,6)
		self.setStaticPoint(2,7,9)
		
		self.setStaticPoint(3,1,8)
		self.setStaticPoint(3,2,3)
		self.setStaticPoint(3,3,2)
		self.setStaticPoint(3,4,6)
		self.setStaticPoint(3,6,4)
		self.setStaticPoint(3,8,9)
		
		self.setStaticPoint(5,0,4)
		self.setStaticPoint(5,2,5)
		self.setStaticPoint(5,4,7)
		self.setStaticPoint(5,5,8)
		self.setStaticPoint(5,6,2)
		self.setStaticPoint(5,7,6)
	
		self.setStaticPoint(6,1,4)
		self.setStaticPoint(6,2,2)
		self.setStaticPoint(6,3,5)
		self.setStaticPoint(6,4,3)
		
		self.setStaticPoint(7,6,7)
		self.setStaticPoint(7,7,2)
		self.setStaticPoint(7,8,4)
		
		self.setStaticPoint(8,0,7)
		self.setStaticPoint(8,2,9)
		self.setStaticPoint(8,3,4)
		self.setStaticPoint(8,5,2)
		self.setStaticPoint(8,7,8)
		
		# self.setStaticPoint(0,1,1)
		# self.setStaticPoint(1,0,2)
		# self.setStaticPoint(1,6,3)
		# self.setStaticPoint(3,5,4)
		# self.setStaticPoint(3,8,5)
		# self.setStaticPoint(5,4,6)
		# self.setStaticPoint(5,7,7)
		# self.setStaticPoint(6,2,8)
		# self.setStaticPoint(6,4,7)
		# self.setStaticPoint(7,2,3)
		# self.setStaticPoint(7,6,2)
		# self.setStaticPoint(8,6,1)	
	# #end def
	
	def solveByAnnealing(self,temperature,coolingRate,iterations):
		print(self.calculateScore())
		score = self.calculateScore()
		for i in range(iterations):
			if(score == 0):
				self.printSudoku()
				print(self.calculateScore())
				return
			#losujemy punkty do zamiany
			(r1,r2) = self.getRandoms()
			self.swapPoints(r1//9,r1%9,r2//9,r2%9)
			tmpScore = self.calculateScore()
			#gdy jest lepiej to zmieniamy // self jest zmieniony juz 
			if tmpScore < score :
				score = tmpScore
				temperature *= coolingRate #zmieniamy temperature
				continue; #szuakmy dalej lepszego rozwiazania
			else :
				#sprawdzamy czy przyjmujemy gorszy wynik
				delta = score - tmpScore #ujemne
				if (numpy.exp(delta/temperature) < random.random() ):
					#wtedy zachowujemy nasz wynik
					score = tmpScore
					temperature *= coolingRate #zmieniamy temperature
					continue; #szuakmy dalej lepszego rozwiazania
				else:
					#teraz go odrzucamy
					self.swapPoints(r1//9,r1%9,r2//9,r2%9)
					temperature *= coolingRate #zmieniamy temperature
		#end for	
		self.printSudoku()
		print(self.calculateScore())
	#end def

#ta funkcja wydaje sie kijowa	
	def getRandoms(self):
		#losujemy wiersz
		row = random.randint(0,8)
		col1 = random.randint(0,8)
		col2 = random.randint(0,8)
		while (col1 == col2) or (self.row[row][col1].getStatic()) or (self.row[row][col2].getStatic()):
			row = random.randint(0,8)
			col1 = random.randint(0,8)
			col2 = random.randint(0,8)
		return (row*9+col1,row*9+col2)
	
	
	
	
	
		# random.seed(time.time()*100000)
		# # random1 = int((time.time()*4096))%80
		# # random2 = int((time.time()*8192))%80
		# random1 = int(random.random()*100)%80
		# random2 = int(random.random()*100)%80
		# while (random1 == random2) or (self.row[random1//9][random1%9].getStatic()) or (self.row[random2//9][random2%9].getStatic()):
			# # if(random1 == random2):
				# # print("xD")
			# while(self.row[random1//9][random1%9].getStatic()):
				# #random1 = random.randint(0,80) 
				# random1 = int(random.random()*100)%80
			# while(self.row[random2//9][random2%9].getStatic()):
				# #random2 = random.randint(0,80)				
				# random2 = int(random.random()*100)%80
			# if(random1 == random2):
				# print("xDDD")
		# return (random1,random2)
	# #end
	
	
#end def class
	
if __name__ == '__main__':
	s = Sudoku()
	s.printSudoku()
	s.setFirst()
	print("I've set first\n")
	s.printSudoku()
	print("After filling sudoku")
	s.fillSudoku2()
	s.printSudoku()
	print("WYNIK")
	s.solveByAnnealing(1000,0.99999,30000)
	#s.solveByAnnealing(1000,0.99999,7000)

	

	
	
	# string = 'string'
	# for i in range(11):
		# string +=str(i)
	# print(string)