from manim import *
import Galaxy
from array import array

class DarkForest(Scene):
	def construct(self):
		'''建议X:Y=7:4'''
		GalSizeX = 35
		GalSizeY = 20
		GalCivilizations = 50
		# reduce animation time
		simple = True

		self.Universe = Galaxy.Galaxy(GalSizeX, GalSizeY, GalCivilizations)
		self.year = Text('')
		self.txts = VGroup()
		self.lines = VGroup()
		self.CivLabels = {}
		self.conveys = []
		

		TConstantX = 7.0/GalSizeX
		TConstantY = 7.0/GalSizeY

		self.CivGroup = {}

		self.updateAge()
		self.initCivs(simple=simple)
		self.initIR(simple=simple)
		self.label()

		# Begin Galaxy Development


		while not self.Universe.end():
			self.Universe.move()
			# self.drawConvey()
			if self.Universe.NewCiv:
				self.addCiv()
			self.drawRelations()
			self.updateAge()
			self.checkChangeAttitude()
			self.drawIR()
			self.checkDead()

		# print(CivGroup)
		self.ending()

	# def drawConvey(self):
		# for i in self.conveys:
		# 	self.remove(i)
		# 	self.conveys.remove(i)

		# for civ in self.Universe.Civilizations:
		# 	for i in civ.Conveys:
		# 		if i.Distance >0:
		# 			if i.Friend:
		# 				c = ImageMobject('conveygreen.png')
		# 				c.rotate((i.Angle-90)*DEGREES)
		# 				c.move_to(i.transformCoord())
		# 				c.scale(0.1)
		# 				self.add(c)
		# 				self.conveys.append(c)
		# 			else:
		# 				c = ImageMobject('conveyred.png')
		# 				c.rotate((i.Angle-90)*DEGREES)
		# 				c.move_to(i.transformCoord())
		# 				c.scale(0.1)
		# 				self.add(c)
		# 				print(i.Rad)
		# 				self.conveys.append(c)
					
	def addCiv(self):
		self.CivGroup[self.Universe.New] = VGroup(Dot(point=ORIGIN, radius=0.05))

		if self.Universe.New.Attitude == 1:
			self.CivGroup[self.Universe.New][0].set_color(GREEN)
		elif self.Universe.New.Attitude == 2:
			self.CivGroup[self.Universe.New][0].set_color(RED)
		elif self.Universe.New.Attitude == 3:
			self.CivGroup[self.Universe.New][0].set_color(YELLOW)
		else:
			self.CivGroup[self.Universe.New][0].set_color(GREY)

		self.play(FadeIn(self.CivGroup[self.Universe.New][0]))
		self.wait(0.1)
		self.play(ApplyMethod(self.CivGroup[self.Universe.New][0].shift, self.Universe.New.transformCoord()), run_time=1)

		IR = Ellipse(width=self.Universe.New.IRadius*(6.8/self.Universe.Xsize), height=self.Universe.New.IRadius*(3.886/self.Universe.Ysize), stroke_width=1)
		self.CivGroup[self.Universe.New].add(IR)
		IR.move_to(self.Universe.New.transformCoord())
		if self.Universe.New.Attitude == 1:
			self.CivGroup[self.Universe.New][1].set_color(GREEN)
		elif self.Universe.New.Attitude == 2:
			self.CivGroup[self.Universe.New][1].set_color(RED)
		elif self.Universe.New.Attitude == 3:
			self.CivGroup[self.Universe.New][1].set_color(YELLOW)
		else:
			self.CivGroup[self.Universe.New][1].set_color(GREY)

		self.play(Create(IR))

		a = self.Universe.New.Name[4:]
		print(a)
		try:
			t = Text(a)
		except Exception:
			t = Text('No. ????')
		t.scale(0.2)
		t.next_to(self.CivGroup[self.Universe.New][0], direction=RIGHT, )
		self.add(t)
		self.CivLabels[self.Universe.New] = t
		self.txts.add(t)

	def drawRelations(self):
		# self.play(FadeOut(self.lines))
		for i in self.lines:
			self.remove(i)
			self.lines.remove(i)

		for civ in self.Universe.Civilizations:
			for war in civ.War:
				l = Line(civ.transformCoord(), war.transformCoord(), stroke_width=0.8).set_color(RED)
				self.lines.add(l)
				self.add(l)
			for ally in civ.Ally:
				l = Line(civ.transformCoord(), ally.transformCoord(), stroke_width=0.8).set_color(GREEN)
				self.lines.add(l)
				self.add(l)		


	def ending(self):
		self.play(FadeOut(self.txts))
		self.play(FadeOut(self.lines))
		self.remove(self.txts)
		for civ in self.Universe.Civilizations:
			self.play(FadeOut(self.CivGroup[civ]))
			self.remove(self.CivGroup[civ])

		civ = self.Universe.Civilizations[0]

		self.WIN = Dot(radius=1)

		if civ.Attitude == 1:
				self.WIN.set_color(GREEN)
		elif civ.Attitude == 2:
			self.WIN.set_color(RED)
		elif civ.Attitude == 3:
			self.WIN.set_color(YELLOW)
		else:
			self.WIN.set_color(GREY)

		self.play(FadeIn(self.WIN))
		self.wait(2)
		info = Text(f'{civ.Name}\nTech: {civ.Tech}\nPower: {round(civ.Power, 2)}\nAttitude: {civ.Attitude}')
		
		info.scale(0.8)
		self.play(ApplyMethod(self.WIN.move_to, LEFT*2.5), run_time=1)
		info.next_to(self.WIN, direction=RIGHT, )
		self.play(FadeIn(info))
		self.wait(4)
		self.play(FadeOut(info), FadeOut(self.WIN))

		self.galaxyStats()

	def galaxyStats(self):
		logo = ImageMobject('galaxy.png', invert=True)
		logo.scale(0.4)
		t = ''
		for i in self.Universe.Stats.keys():
			t+= str(i)+': '+str(round(self.Universe.Stats[i],2))+'\n'

		info = Text(t)
		info.scale(0.8)
		
		self.play(FadeIn(logo))
		self.play(ApplyMethod(logo.move_to, LEFT*2))
		info.next_to(logo, direction=RIGHT)
		self.play(FadeIn(info))
		self.wait()
		
		


	def checkDead(self):
		if(len(self.Universe.Dead)>0):
			for civ in self.Universe.Dead:
				self.play(FadeOut(self.CivGroup[civ][0]), FadeOut(self.CivGroup[civ][1]), FadeOut(self.CivLabels[civ]))

				self.remove(self.CivGroup[civ])
				self.CivGroup.pop(civ)
				self.Universe.Dead.remove(civ)


	def updateAge(self):
		past = self.year
		self.remove(past)

		self.year = Text(f"{self.Universe.age*10}", aligned_edge=LEFT).set_color(WHITE)
		self.year.shift(LEFT*6+UP*3)
		self.add(self.year)
		

	def checkChangeAttitude(self):
		for civ in self.Universe.Civilizations:
			if civ.Attitude == 1:
				self.CivGroup[civ][0].set_color(GREEN)
			elif civ.Attitude == 2:
				self.CivGroup[civ][0].set_color(RED)
			elif civ.Attitude == 3:
				self.CivGroup[civ][0].set_color(YELLOW)
			else:
				self.CivGroup[civ][0].set_color(GREY)

	def label(self):
		for civ in self.Universe.Civilizations:
			a = civ.Name[4:]
			print(a)
			try:
				t = Text(a)
			except Exception:
				t = Text('No. ????')
			t.scale(0.2)
			# t.move_to(civ.transformCoord()+RIGHT*0.4)
			t.next_to(self.CivGroup[civ][0], direction=RIGHT, )
			self.add(t)
			self.CivLabels[civ] = t
			self.txts.add(t)

	def drawIR(self):
		for civ in self.Universe.Civilizations:
			IR = Ellipse(width=civ.IRadius*(6.8/self.Universe.Xsize), height=civ.IRadius*(3.886/self.Universe.Ysize), stroke_width=1)
			past = self.CivGroup[civ][1]
			self.CivGroup[civ].remove(past)
			self.remove(past)
			self.CivGroup[civ].add(IR)
			IR.move_to(civ.transformCoord())
			if civ.Attitude == 1:
				self.CivGroup[civ][1].set_color(GREEN)
			elif civ.Attitude == 2:
				self.CivGroup[civ][1].set_color(RED)
			elif civ.Attitude == 3:
				self.CivGroup[civ][1].set_color(YELLOW)
			else:
				self.CivGroup[civ][1].set_color(GREY)
			self.add(IR)
			# self.wait(0.5)
		self.wait()

	def initIR(self, simple=False):
		for civ in self.Universe.Civilizations:
			IR = Ellipse(width=civ.IRadius*(6.8/self.Universe.Xsize), height=civ.IRadius*(3.886/self.Universe.Ysize), stroke_width=1)
			self.CivGroup[civ].add(IR)
			IR.move_to(civ.transformCoord())
			if civ.Attitude == 1:
				self.CivGroup[civ][1].set_color(GREEN)
			elif civ.Attitude == 2:
				self.CivGroup[civ][1].set_color(RED)
			elif civ.Attitude == 3:
				self.CivGroup[civ][1].set_color(YELLOW)
			else:
				self.CivGroup[civ][1].set_color(GREY)

			if not simple:
				self.play(Create(IR))
			else:
				self.add(IR)
			# self.wait(0.5)
		self.wait()


	def initCivs(self,simple=False):
		if not simple:
			for civ in self.Universe.Civilizations:

				self.CivGroup[civ] = VGroup(Dot(point=ORIGIN, radius=0.05))

				if civ.Attitude == 1:
					self.CivGroup[civ][0].set_color(GREEN)
				elif civ.Attitude == 2:
					self.CivGroup[civ][0].set_color(RED)
				elif civ.Attitude == 3:
					self.CivGroup[civ][0].set_color(YELLOW)
				else:
					self.CivGroup[civ][0].set_color(GREY)

				self.play(FadeIn(self.CivGroup[civ][0]))
				self.play(ApplyMethod(self.CivGroup[civ][0].move_to, civ.transformCoord()), )
				# self.wait(0.1)
			self.wait(1)
		else:
			for civ in self.Universe.Civilizations:

				self.CivGroup[civ] = VGroup(Dot(point=ORIGIN, radius=0.05))

				if civ.Attitude == 1:
					self.CivGroup[civ][0].set_color(GREEN)
				elif civ.Attitude == 2:
					self.CivGroup[civ][0].set_color(RED)
				elif civ.Attitude == 3:
					self.CivGroup[civ][0].set_color(YELLOW)
				else:
					self.CivGroup[civ][0].set_color(GREY)

				self.CivGroup[civ][0].move_to(civ.transformCoord())
				self.add(self.CivGroup[civ][0])




		# Contruct Universe with initial Civilizations
		# for i in Universe.Civilizations:
		# 	CivDot[i] = Dot(point=[i.X, i.Y, 0], radius=0.08, )
		# 	self.play(FadeIn(CivDot[i]))


		





	
	