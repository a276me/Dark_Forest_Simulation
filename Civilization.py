import random
import math
import Galaxy
import Convey
import Request
from manim import *


class Civilization:
	'''
	文明类：
		在宇宙中的坐标X,Y
		文明性格：
			1 = 积极友好
				-主动向在影响范围之内的被发现文明提出结盟请求
				-发出请求后会被接受文明发现
				-绝不先开战
			2 = 好战
				-见到文明就打
				-被发现概率极高
				-每次派出战舰的数量与实力的百分比极高
				-战争消耗极小
			3 = 闭关锁国
				-被发现几率很低
				-尽量鼓励自己
			4 = 中立
				-不结盟
				-不主动出击

		结盟特性:
			如果与一个实力大于自己两倍的文明将会求救于结盟的文明
			每次申请只会援助一次
			每次援助将会赠送援助国5%的实力
			结盟的国家越多科技和实力提升的越快

		外交：
			不管是进攻还是援助，都会排出舰队
			舰队速度取决于文明科技

		科技：
			文明实力从来都不是线性增长
			科技等级越高实力增长得越快
			每回合文明科技进步几率为5%
			每次进步科技指数会增长0.1
			！没有上限

		实力：
			实力的增加是指数性的
			每回合增加的数量是上回会乘以（1+（科技+盟友数量）%）
			实力为0的时候文明灭亡
			！没有上限

		影响范围：
			若其他文明在一个文明的影响范围之内将有一定几率被发现
				积极友好，中立 = 20%
				闭关锁国 = 5%
				好战 = 50%
			影响范围 = sqrt(实力)

		进攻：
			敌对文明互相进攻时会派出自己一定比例的实力来进攻
				中立，闭关锁国 = 20%
				友好 = 17.5%
				好战 = 22.5%
			消耗实力 = 进攻实力/2
			进攻消耗如下：
				中立，闭关锁国 = 10%
				友好 = 9.75%
				好战 = 11.25%
		
		随机事件：
			每回合0.5%科技爆发 科技+1
			每回合0.5%科技倒车 科技-0.5
				若小于0.6则直接归零
			每回合0.1%内乱 	  实力-50% 科技-0.5
			每回合5%政治动荡   文明性格改变
			每回合1%社会动荡	  实力-25%

			如果任何一项触发，文明自动跳过回合


	'''

	def __init__(self, Gal):
		self.Galaxy = Gal
		self.setCoord(Gal)
		self.Tech = random.randint(0,20) / 10.0		# 宇宙从来都不是公平的
		self.Power = random.randint(0, int(self.Galaxy.Xsize+self.Galaxy.Ysize))
		self.getname()
		self.IRadius = 1
		self.Alive = True
		self.Attitude = self.setAttitude()
		self.KnownCivs = [] #已知文明
		self.War = []
		self.Ally = []
		self.Conveys = []
		self.diplomaticRequests = []


	def move(self):
		if self.Power <=0:
			self.Alive = False
		if self.Alive:
			if(self.event()):
				return
			else:
				self.special()
				self.improveTech()
				self.improvePower()
				self.updateIR()
				self.discover()
				self.interact()
				self.receiveConvey()
				self.military()
				self.aidAllies()
		else:
			self.Galaxy.removeCiv(self)


	def __str__(self):
		return f'{self.Name}; \t\tTech: {self.Tech}; \t\tPower: {self.Power}; \t\tIRadius: {self.IRadius}; \t\tCoord: ({self.X}, {self.Y}); \t\tDiscovered: {len(self.KnownCivs)}; \t\tWars: {len(self.War)}; \t\tAttitude: {self.Attitude}; \t\tAllies: {len(self.Ally)}'

	def special(self):
		'''如果已经是称霸文明'''
		largest = True
		for i in self.Galaxy.Civilizations:
			if self.Power<i.Power*2:
				largest = False
		if largest:
			'''如果是就会对所有文明发动战争'''
			self.changeAttitude()


	def interact(self):
		if self.Attitude == 2:
			for i in self.KnownCivs:
				'''对已经被发现且实力比自己低的文明发动战争'''
				if (i not in self.War) and i.Power<=self.Power*2:
					i.declareWar(self)
		else:
			for i in self.War:
				'''热爱和平或者中立文明不喜欢战争除非信心打赢这场战争'''
				if (i.Power>self.Power *1.3 or i.Tech-self.Tech >= 0.5):
					i.stopWar(self)

	def getname(self):
		while True:									# 确保文明坐标不重合
			notEq = True
			self.Name = 'Civ No. '+str(random.randint(1000,10000))
			for i in self.Galaxy.Civilizations:
				if i is not self and i.Name == self.Name:
					notEq = False
			if notEq:
				break

	def changeAttitude(self, new=2):
		if new == 2:
			'''突然变得好战'''
			for i in self.Ally:
				i.cancelAlliance(self)
			for i in self.KnownCivs:
				if i not in self.War:
					i.declareWar(self)
		if new == 1:
			'''突然变得友好'''
			for i in self.KnownCivs:
				i.requestAlliance(self)

		if new == 3 or new == 4:
			for i in self.Ally:
				i.cancelAlliance(self)

	def cancelAlliance(self, sender):
		if sender in self.Ally:
			self.Ally.remove(sender)
			sender.Ally.remove(self)

	def aidAllies(self):
		for i in self.diplomaticRequests:
			if self.Power >= self.Tech*10:
				'''cant aid others if you are to weak'''
				i.Target.sendConvey(self, True)
			self.diplomaticRequests.remove(i)

	def askAid(self):
		for i in self.Ally:
			i.sendRequest(self)

	def stopWar(self,sender):
		if sender in self.War:
			self.War.remove(sender)
			sender.War.remove(self)
			self.Galaxy.Stats['Cease Fires'] += 1
			# 撤回舰队
			for i in self.Conveys:
				if i.Sender is sender:
					self.Conveys.remove(i)
			for i in sender.Conveys:
				if i.Sender is self:
					sender.Conveys.remove(i)


	def military(self):
		'''take military actions against other countries'''
		aid = False
		for i in self.War:
			i.sendConvey(self, False)
			if (i.Power >= self.Power*1.5 or i.Tech-self.Tech >0.5) and aid == False:
				self.askAid()
				aid = True

	def sendConvey(self, sender, friendly):
		'''the sender sends a convey to the object who's function gets called'''
		self.Conveys.append(Convey.Convey(self, sender, friendly))
	
	def sendRequest(self, asker):
		self.diplomaticRequests.append(Request.Request(asker, self))

	def receiveConvey(self):
		'''receive ships/conveys from other civilizations'''
		for i in self.Conveys:
			if i.Distance <= 0:
				self.Power -= i.Power
				self.Conveys.remove(i)
			else:
				i.move()

	def transformCoord(self):
		return RIGHT*self.X*(6.8/self.Galaxy.Xsize) + UP*self.Y*(3.886/self.Galaxy.Ysize)

	def transformX(self):
		return self.X*(6.8/self.Galaxy.Xsize)

	def transformY(self):
		return self.Y*(3.886/self.Galaxy.Ysize)

	def know(self, civ):
		if civ not in self.KnownCivs:
			self.KnownCivs.append(civ)

	def discover(self):
		Civs = self.Galaxy.getCivilizations(self.X, self.Y, self.IRadius)
		for i in Civs:
			if i in self.KnownCivs:
				continue
			if i.Attitude == 1 or i.Attitude == 4: # 积极，中立  20%
				if random.randint(0,100) < 20:
					self.KnownCivs.append(i)
					self.diplomacy(i)

			elif i.Attitude == 3:				   # 闭关锁国    5%
				if random.randint(0,100) < 5:
					self.KnownCivs.append(i)
					self.diplomacy(i)

			elif i.Attitude == 2:				   # 好战	   50%
				if random.randint(0,100) < 50:
					self.KnownCivs.append(i)
					self.diplomacy(i)

	def diplomacy(self, recp):
		if self.Attitude == 2:					   # 好战	直接发动战争
			recp.declareWar(self)
		elif self.Attitude == 1:				   # 友好	发出结盟请求
			recp.requestAlliance(self)


	def declareWar(self, sender):
		self.War.append(sender)
		sender.War.append(self)
		self.know(sender)
		self.Galaxy.Stats['Wars'] +=1

	def requestAlliance(self, sender):
		if self.Attitude == 1 and sender not in self.Ally:					  # 友好态度才接受结盟
			self.Ally.append(sender)
			sender.Ally.append(self)
		self.know(sender)

	def setAttitude(self):
		choice = random.randint(0,10)
		if choice < 1:
			return 4
		elif choice < 5:
			return 1
		elif choice < 9:
			return 2
		elif choice < 11:
			return 3

	def updateIR(self):
		self.IRadius = round(math.sqrt(self.Power/2.0),2)

	def improveTech(self):
		if random.randint(0,100)<5:
			self.Tech+=0.1
			self.Tech = round(self.Tech,2)
	def improvePower(self):
		self.Power *= 1.0+((self.Tech+len(self.Ally))/100.0)
		self.Power = round(self.Power,6)

	def setCoord(self, Gal):
		while True:									# 确保文明坐标不重合
			notEq = True
			self.X = round(2*self.Galaxy.Xsize*random.random()-self.Galaxy.Xsize, 2)
			# -Galaxy.size < x < Galaxy.size
			self.Y = round(2*self.Galaxy.Ysize*random.random()-self.Galaxy.Ysize, 2)
			for i in Gal.Civilizations:
				if i is not self and i.X == self.X and i.Y == self.Y:
					notEq = False
			if notEq:
				break


	def event(self):
		choice = random.randint(0,1000)
		if choice < 5:
			# Tech explosion
			self.Tech +=1
			return True

		if choice >= 5 and choice <10:
			# Tech Deprecation
			if self.Tech >0.5:
				self.Tech -= 0.5
			else:
				self.Tech = 0
			return True
			
		if choice == 11:
			# Civil War
			self.Power *= 0.5
			if self.Tech > 0.5:
				self.Tech -=0.5
			else:
				self.Tech = 0

			self.Galaxy.Stats['Civil Wars'] += 1
			return True
			
		if choice > 11 and choice < 66:
			# ideology Change
			change = self.setAttitude()
			while change == self.Attitude:
				change = self.setAttitude()
			self.Attitude = change
			self.changeAttitude(new=change)
			return True

		if choice >=66 and choice<76:
			# Social Unrest
			self.Power*=0.75
			return True
			
		return False

	


		




