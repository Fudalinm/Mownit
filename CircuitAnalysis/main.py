#• Wariant na ocenę 5.0:
######################################
# Przygotuj program pozwalający na analizę obwodu elektrycznego z wykorzystaniem II
# prawa Kirchhoffa. Dane wejściowe to graf opisujący układ połączeń układu
# elektrycznego wraz z oporami, lista krotek (a,b,E) opisujących między którymi
# węzłami przyłożono jaką SEM, oraz opór elektryczny poszczególnych połączeń. Na
# wyjściu program powinien wygenerować graf ważony, gdzie waga krawędzi powinna
# odpowiadać natężeniu prądu na odpowiadającym jej połączeniu w obwodzie.


#nasz graf bedzie opisany nastepujaco
#2 rodzaje krotek	
	# polaczenie opornikowe
		# reprezentowana przez (a,b,R) 
		# a - punkt
		# b - punkt 
		# R - rezystancja oporu na danym polaczeniu wyrazona w omach
	# polaczenie napciowe
		# reprezentowane przez krotke (a,b,V)
		# a - punkt
		# b - punkt 
		# V - reprezentuje wartosc zrodla napiecia wyrazona w V napiecie przylozone z a do b
#zasada działania programu
	#program pobiera liste krotek
	#na jej podstawie budowany jest graf
	#w grafie znajdujemy cyckle
		#redukujemy zbior cyckli do zbioru cykli znaczacych z punktu widzenia programu
	#na podstawie kazdego znaczacego cyklu tworzymy pojedyncze rownanie
	#na podstawie otrzymanych macierzy otrzymujemy wyniki
	#wypisujemy wszystko na grafie
	
import numpy
import matplotlib.pyplot as plt
#import networkx as nx
import pylab

class ResistanceLink():
	def __init__(self, a , b , R):
		self.point1 = a;
		self.point2 = b;
		self.Resistance = R;
		self.current = 0; #ujemny prad oznacza bieg pradu z point2 do point1 
	#end init
	def __str__(self):
		return "(%d,%d,%d O,%f A)" % (self.point1, self.point2,self.Resistance,self.current)
	def __repr__(self):
		return "(%d,%d,%d O,%f A)" % (self.point1, self.point2,self.Resistance,self.current)
#end class

class VoltageLink():
	def __init__(self , a , b , V):
		self.point1 = a;
		self.point2 = b;
		self.Voltage = V;
	#end init
	def __str__(self):
		return "(%d,%d,%d V)" % (self.point1, self.point2,self.Voltage)
	def __repr__(self):
		return "(%d,%d,%d V)" % (self.point1, self.point2,self.Voltage)
#end class

class Circuit():
	def __init__ (self, VoltageLinkList, ResistanceLinkList):
		self.voltageSources = [];
		self.Resistors = [];
		for x in VoltageLinkList:
			self.voltageSources.append((x,[]))
		#end for
		for x in ResistanceLinkList:
			self.Resistors.append((x,[]))
		#end for
		#inicjalizacja grafu
		self.graph = {}
		#musimy zainicjalizowac to jako liste
		for x in VoltageLinkList:
			self.graph[x.point1] = []
			self.graph[x.point2] = []
		#end for
		for x in ResistanceLinkList:
			self.graph[x.point1] = []
			self.graph[x.point2] = []
		#przypisanie wrtosci do grafu
		#warning czy napewno wszystkie dodalem?!
		#dodajemy kazdy punkt i jego liste polaczen z innymi 
		for x in VoltageLinkList:
			self.graph[x.point1].append(x.point2);#tutaj sobie na biezaco tworzymy graf
			self.graph[x.point2].append(x.point1);#tutaj sobie na biezaco tworzymy graf
		#end for
		for x in ResistanceLinkList:
			self.graph[x.point1].append(x.point2);#tutaj sobie na biezaco tworzymy graf
			self.graph[x.point2].append(x.point1);#tutaj sobie na biezaco tworzymy graf
		#end for
	#end init
	#sprawdzic
	def findAllCycles(self):
		#result to lista cykli z czego kazdy cykl jest zapisany jako lista
		return [[node]+path  for node in self.graph for path in dfs(self.graph, node, node)];	
	#end method		
#end class

def dfs(graph, start, end):
	fringe = [(start, [])]
	while fringe:
		state, path = fringe.pop()
		if path and state == end:
			yield path
			continue
		for next_state in graph[state]:
			if next_state in path:
				continue
			fringe.append((next_state, path+[next_state]))
#end method	

def ifSameCycle(cycleA,cycleB):
	if (len(cycleA) != len(cycleB)):
		return False;
	#end if
	try:
		index = cycleB.index(cycleA[0]);
	except:
		return False;
	#end try	
	for i in range(len(cycleA)):
		if cycleA[i] != cycleB[ (index+i)%len(cycleB) ]:
			return False;
		#end if
	#end for
	return True;
#end def

def ifResAndLinksInLoop(resAndLinks,loopId):
	try:
		resAndLinks[1].index(loopId)
	except:
		return False
	return True
#end def

#mamy wszystkie cykle teraz chcielibysmy ulozyc z nich rownania
def createEquations(loops,circuit):
	#mamy tyle uk
	matrix = [] # matrix will be fo [[]] type, and matrix[0][1] let's assume 0 row, and 1 column
	vector=[]
	for x in range(len(loops)):#create vector with 0
		vector.append(0)
	for x in range(len(loops)): # create N rows
		matrix.append([])
		for k in range(len(loops)):# fill N rows with 0
			matrix[x].append(0)
	for generalLoopId in range(len(loops)): #dla kazdego znalezionego oczka (bierzemy sobie jego index)
		for resAndLinks in filter(lambda resTuple : generalLoopId in resTuple[1] ,circuit.Resistors):#bierzemy wszystkie rezystory znajdujace sie w danym oczku
			matrix[generalLoopId][generalLoopId] += resAndLinks[0].Resistance #dodajemy opor kazdego opornika w danym oczku
			for loopsForRes in filter(lambda x: x != generalLoopId, resAndLinks[1]):
				if fPositive(resAndLinks[0],loops[loopsForRes]) == fPositive( resAndLinks[0],loops[generalLoopId] ): # sprawdzamy kierunek pradu w petli z kierunkiem w petli glownej
					#jezeli sa te same kierunki to dodaje
					matrix[generalLoopId][loopsForRes] += resAndLinks[0].Resistance # add to given column
				else:
					#jezeli przeciwne to odejmuje
					matrix[generalLoopId][loopsForRes] -= resAndLinks[0].Resistance # remove from given column	
	for volAndLoops in circuit.voltageSources:
		for loopsForVolt in volAndLoops[1]:
			if fPositiveVoltage(volAndLoops[0],loops[loopsForVolt]):
				vector[loopsForVolt]+=volAndLoops[0].Voltage
			else:
				vector[loopsForVolt]-=volAndLoops[0].Voltage	
	return (matrix,vector)
#end def

def filterBySize(listOfLists,size):
	for x in range(len(listOfLists)):
		if len(listOfLists[x]) > size:
			continue
		else:
			listOfLists[x] = []
	#end for
	return listOfLists
#end def

def reduce(listOfCycles):
	#usuniecie pierwszego elementu z kazdej listy
	#listOfCycles = filter(lambda x: len(x) > 3,listOfCycles )
	listOfCycles = filterBySize(listOfCycles,3)
	for x in listOfCycles:
		if(len(x) > 0):
			x.pop(0);
	#end for
	for x in range(0,len(listOfCycles)):
		for y in range(x+1,len(listOfCycles)):
			if ifSameCycle(listOfCycles[x],listOfCycles[y]) or ifSameCycle(listOfCycles[x],listOfCycles[y][::-1]):
				listOfCycles[y] = [];
		#end for
	#end for
	#usuwamy puste listy
	return [x for x in listOfCycles if x != []]
#end def

def ifInCycle(point1,point2,cycle):
	try:
		index1 = cycle.index(point1);
		index2 = cycle.index(point2);
		if (index1 + 1)%len(cycle) == (index2)%len(cycle) or (index1 - 1)%len(cycle) == (index2)%len(cycle):
			return True;
		#end if
	except:
		return False;
	#end try
	return False
#end def
	
def asignCyclesToLinks(loops,resistors,voltageSources):
	for x in range(len(loops)):
		index = x
		for y in resistors:
			if ifInCycle(y[0].point1,y[0].point2,loops[x]):
				y[1].append(index);	
		#end for
		for y in voltageSources:
			if ifInCycle(y[0].point1,y[0].point2,loops[x]):
				y[1].append(index);	
		#end for
	#end for
#end def
	
def isInCycle(i,loopsAttended):
	try:
		loopsAttended.index(i)
		return True
	except:
		return False
#end def

		
def fPositive(res,loop):
	id=loop.index(res.point1)
	if loop[(id+1)%len(loop)] == res.point2 :
		return True
	else:
		return False
#edn def
	
def fPositiveVoltage(volt,loop):
	id=loop.index(volt.point1)
	if loop[(id+1)%len(loop)] == volt.point2 :
		return True
	else:
		return False
#end def 	


def assignCurrentToResistor(ResistanceLinkList,loops,x):
	for resistorTouple in ResistanceLinkList:
		for loopIndex in resistorTouple[1]:
			if fPositive(resistorTouple[0],loops[loopIndex]):
				resistorTouple[0].current += x[loopIndex]
			else:
				resistorTouple[0].current -= x[loopIndex]
			#end if
		#end for	
	#end for
	for r in ResistanceLinkList:
		print(r[0]);
	#end for
#end def
	
def solveEquations(A,b):
	A2 = numpy.array(A)
	b2 = numpy.array(b)
	print("Dostarczone macierze\n A:")
	print(A2)
	print("b:")
	print(b2)
	#nie mozemy tego uzyc poniewaz czasem jest wiecej niz jedno rozwiazanie
	#x = numpy.linalg.solve(A2,b2)
	x = numpy.linalg.lstsq(A2, b2,rcond=-1)[0]
	print("x:")
	print(x)
	return x;	
#end def


def printCircuit(Circuit):
	#tworzenie grafu
	G = nx.DiGraph()
	#dodanie krawedzi
	for rt in Circuit.Resistors: #dla kazdej tupli rezysor prad
		if rt[0].current  > 0:
			G.add_edges_from([ (rt[0].point1,rt[0].point2) ], weight = rt[0].current)
		else:
			G.add_edges_from([ (rt[0].point2,rt[0].point1) ], weight = -rt[0].current)
		#end if
	#end for
	for vt in Circuit.voltageSources: #dla kazdej tupli rezysor prad
			G.add_edges_from([ (vt[0].point1,vt[0].point2) ], weight = vt[0].Voltage)
		#end if
	#end for
	edge_labels=dict([((u,v,),d['weight']) for u,v,d in G.edges(data=True)])		 
	pos=nx.spring_layout(G)
	nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
	nx.draw(G,pos,  node_size=1500,edge_color='black')
	pylab.show()	
#end def

def runGeneralSolving(voltageLinkList,resistorsLinkList):
	#tworzymy obwód
	Circuit1 = Circuit(voltageLinkList,resistorsLinkList)
	
	#wyprintujmy sobie graf
	#print(Circuit1.graph);
	#print(Circuit1.findAllCycles());
	loops = reduce(Circuit1.findAllCycles())
	asignCyclesToLinks(loops,Circuit1.Resistors,Circuit1.voltageSources);
	print(loops);
	# print("\n")
	# print(Circuit1.Resistors);
	# print("\n")
	# print(Circuit1.voltageSources);
	# print("\n")
	
	(A,b) = createEquations(loops,Circuit1)
	x = solveEquations(A,b)
	assignCurrentToResistor(Circuit1.Resistors,loops,x)
	#printCircuit(Circuit1)
#end def
	
def runFirstExample():
	#tworzymy rezystory
	resistorsLinkList = []
	resistorsLinkList.append(ResistanceLink(2,3,5))
	resistorsLinkList.append(ResistanceLink(3,4,5))
	resistorsLinkList.append(ResistanceLink(4,1,5))
	resistorsLinkList.append(ResistanceLink(3,5,5))
	resistorsLinkList.append(ResistanceLink(5,6,5))
	resistorsLinkList.append(ResistanceLink(6,4,5))
	#tworzymy napiecie
	voltageLinkList = []
	voltageLinkList.append(VoltageLink(1,2,20))
	runGeneralSolving(voltageLinkList,resistorsLinkList)
	return
#end def		
	
def runSecondExample():
	#tworzymy rezystory
	resistorsLinkList = []
	resistorsLinkList.append(ResistanceLink(2,3,10))
	resistorsLinkList.append(ResistanceLink(3,4,20))
	resistorsLinkList.append(ResistanceLink(3,8,15))
	resistorsLinkList.append(ResistanceLink(8,9,25))
	resistorsLinkList.append(ResistanceLink(9,10,35))
	resistorsLinkList.append(ResistanceLink(8,7,5))
	resistorsLinkList.append(ResistanceLink(1,5,30))
	resistorsLinkList.append(ResistanceLink(5,6,40))
	
	#tworzymy napiecie
	voltageLinkList = []
	voltageLinkList.append(VoltageLink(1,2,1000))
	voltageLinkList.append(VoltageLink(5,4,1000))
	voltageLinkList.append(VoltageLink(6,7,2000))
	voltageLinkList.append(VoltageLink(6,10,2000))

	runGeneralSolving(voltageLinkList,resistorsLinkList)
	return
#end def	

def runThirdExample():
	#tworzymy rezystory
	resistorsLinkList = []
	resistorsLinkList.append(ResistanceLink(1,2,0))
	resistorsLinkList.append(ResistanceLink(2,3,0))
	resistorsLinkList.append(ResistanceLink(3,4,1))
	resistorsLinkList.append(ResistanceLink(4,5,0))
	resistorsLinkList.append(ResistanceLink(5,6,0))
	resistorsLinkList.append(ResistanceLink(2,5,1000000))
	
	#tworzymy napiecie
	voltageLinkList = []
	voltageLinkList.append(VoltageLink(6,1,10))
	
	runGeneralSolving(voltageLinkList,resistorsLinkList)
	return;
#end def
	
if __name__ == "__main__":

	runFirstExample()
	#runSecondExample()
	#runThirdExample()
