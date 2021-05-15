import Galaxy
import Tools
from manim import *
import math

class Convey:
	def __init__(self, target, sender, friendly):
		self.Speed = sender.Tech*2
		self.Distance = Tools.getDistance(sender, target)
		self.Friend = friendly
		self.Target = target
		self.Sender = sender
		# self.Quad = Tools.getQuad(self.Sender, self.Target)
		self.X = self.Sender.X
		self.Y = self.Sender.Y
		# self.Angle = Tools.calculateAngle(self.Sender, self.Target, self)
		# self.Rad = self.Angle*(math.pi/180)
		self.setPower()

		self.Sender.Galaxy.Stats['Conveys'] +=1
		if self.Friend:
			self.Sender.Galaxy.Stats['Ally Aids'] += abs(self.Power)

	def transformCoord(self):
		return RIGHT*self.X*(6.8/self.Sender.Galaxy.Xsize) + UP*self.Y*(3.886/self.Sender.Galaxy.Ysize)


	def setPower(self):
		if self.Friend:
			self.Power = 0-self.Sender.Power*0.05
			self.Sender.Power *= 0.95
		else:
			if self.Sender.Attitude == 1:
				self.Power = self.Sender.Power * 0.175
				self.Sender.Power *= 0.9125
			elif self.Sender.Attitude == 2:
				self.Power = self.Sender.Power * 0.3
				self.Sender.Power *= 0.9
			elif self.Sender.Attitude == 3 or self.Sender.Attitude == 4: 
				self.Power = self.Sender.Power * 0.2
				self.Sender.Power *= 0.9

	def __str__(self):
		return f'Convey; SentBy: {self.Sender.Name}; Recipitant: {self.Target.Name} Friendly: {self.Friend}; Power: {self.Power}; Distance: {self.Distance}'

	def move(self):
		self.Distance -= self.Speed
		# self.X += self.Speed * math.cos(self.Rad)
		# self.Y += self.Speed * math.sin(self.Rad)
		# if self.Quad == 1:
		# 	self.X += self.Speed * math.cos(self.Rad)
		# 	self.Y += self.Speed * math.sin(self.Rad)
		# elif self.Quad == 2:
		# 	self.X += self.Speed * math.cos(self.Rad)
		# 	self.Y += self.Speed * math.sin(self.Rad)
		self.Distance = round(self.Distance,2)








