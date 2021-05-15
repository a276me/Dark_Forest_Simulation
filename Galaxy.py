import math
import random
import Civilization

class Galaxy:
	def __init__(self, x : int , y: int, InitCivs: int, MaxCivs=100):
		self.Civilizations = []
		self.Dead = []
		self.Max = MaxCivs
		self.Xsize = x
		self.Ysize = y
		self.NewCiv = False
		self.New = 0
		self.age = 0
		self.Stats = {'Wars':0, 'Cease Fires':0, 'Civilizations':0, 'Conveys':0, 'Ally Aids':0, 'Civil Wars':0}
		for i in range(InitCivs):
			self.Civilizations.append(Civilization.Civilization(self))
			print(self.Civilizations[-1].transformCoord())
			self.Stats['Civilizations'] +=1

	def newCiv(self):
		self.NewCiv = False
		if random.randint(0,100) < 1:
			new = Civilization.Civilization(self)
			self.New = new
			self.Civilizations.append(new)
			self.NewCiv = True
			self.Stats['Civilizations'] +=1

	def removeCiv(self, civ):
		# remove Civ if civilization is dead
		print(civ.Name+' Has been Destroyed')
		self.Dead.append(civ)
		self.Civilizations.remove(civ)

		# remove the civ from all War lists
		for i in self.Civilizations:
			if civ in i.War:
				i.War.remove(civ)

		# remove the civ from knownCivs list
		for i in self.Civilizations:
			if civ in i.KnownCivs:
				i.KnownCivs.remove(civ)

		for i in self.Civilizations:
			if civ in i.Ally:
				i.Ally.remove(civ)

	def end(self):
		if len(self.Civilizations)<=1:
			return True
		else:
			return False

	def getTotalConveys(self):
		ret = []
		for i in self.Civilizations:
			for c in i.Conveys:
				ret.append(c)
		return ret

	def move(self):
		self.newCiv()
		for i in self.Civilizations:
			i.move()
			print(i)
		self.age +=1

	def getCivilizations(self, x,y,r):
		ret = []
		for i in self.Civilizations:
			if x == i.X and y == i.Y:
				continue
			elif math.sqrt(((i.X-x)**2)+((i.Y-y)**2)) <= r:	#勾股定理来求范围
				ret.append(i)
		return ret

	def getDistance(self, civ1, civ2):
		return round(math.sqrt(((civ1.X-civ2.X)**2)+((civ1.Y-civ2.Y)**2)), 2)


if __name__ == '__main__':

	Gal = Galaxy(10,10,10)

	while True:
		Gal.move()
		print('***************')
		for i in Gal.getTotalConveys():
			print(i)
		print('---------------')
		input()


# Humans = Civilization(100,100)

# for i in range(10000):
# 	Humans.move()
# 	print(f'Year:{i}; Power:{Humans.Power}; Tech:{Humans.Tech}; attitude:{Humans.Attitude}')

