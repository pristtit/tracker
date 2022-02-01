import neat
import visualize
import pickle
from PIL import Image, ImageDraw, ImageColor


class Test():

	def __init__(self, conf):

		self.config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
		                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
		                         conf)
		self.p = neat.Population(self.config)
		self.p.add_reporter(neat.StdOutReporter(True))
		self.stats = neat.StatisticsReporter()
		self.p.add_reporter(self.stats)

	def chek(self, i, x, y,shag, dic, line):

		vector = [10, 10, -10, -10]
		if i == 0 or i == 2:
			y += vector[i]
		else:
			x += vector[i]
		nomer = str(int(x//shag)) + str(int(y//shag))

		try:
			numberline = list(dic[nomer])
		except KeyError:
			return 0
		for i in numberline:
			try:
				k = int((line[i][3] - line[i][1]) / (line[i][2] - line[i][0]))
				b = line[i][1] - k*line[i][0]
				t = 1
			except ZeroDivisionError:
				b = line[i][1]
				k = line[i][3] - line[i][1]
				t = 0
			for n in range(abs(k) + 1):
				if x >= line[i][0] and x <= line[i][2] and k*x*t + b +n == y:
					return 1
		return 0

	def modulation(self, genome, config, x, y, xx, yy,
					shag, dic, line, popitki, regim=True):

		dark = []
		ty = neat.nn. FeedForwardNetwork.create(genome, config)
		ygebil = 0
		povorot = set()
		for l in range(popitki):
			daun= -l
			povtor = dark.count([x,y])
			#if povtor > ygebil:
			#	ygebil = povtor
			if povtor > 2:
				daun = -popitki
				break
			if povtor > 1:
				ygebil += povtor
			dark.append([x,y])

			if yy >= xx + y -x:
				if yy >= -xx +y + x:
					v = [1,0,0,0]
				else:
					v = [0,0,0,1]
			else:
				if yy >= -xx + y + x:
					v = [0,1,0,0]
				else:
					v = [0,0,1,0]

			for i in range(4):
				v.append(self.chek(i, x, y, shag, dic, line))
			v.append(povtor**2)

			move = ty.activate(v)
			best = move.index(max(move))
			povorot.add(best)

			if v[4 + best] == 1:
				continue
			if 1 in v[4:8]:
				ygebil -= 1
				if ygebil < -20:
					ygebil= -20
			if best == 1:
				x += 10
			elif best == 0:
				y += 10
			elif best == 3:
				x -= 10
			elif best == 2:
				y -= 10
			if x == xx and y == yy:
				break
		if regim:
			return daun - ygebil - (4 - len(povorot))*10
		else:
			return dark


	def visual(self, vhod,vihod,wingen,w,h,x,y,xx,yy,shag,dic,line,popitki):

		vh = [i for i in range(-1,-vhod-1,-1)]
		vh.extend([i for i in range(vihod)])
		node_names = {x:str(x) for x in vh}
		visualize.draw_net(self.config, wingen, True, node_names=node_names, fmt='png')
		#visualize.plot_stats(self.stats, ylog=False, view=True)
		#visualize.plot_species(self.stats, view=True)
		im = Image.new('RGB', (w+5,h+5),(0,0,0))
		dr = ImageDraw.Draw(im)
		dr.rectangle((x-5,h-y-5,x+5,h-y+5), fill=ImageColor.getrgb('red'))
		dr.rectangle((xx-5,h-yy-5,xx+5,h-yy+5), fill=ImageColor.getrgb('blue'))
		for a,b,c,d in line:
			dr.line((a,h-b,c,h-d), fill=ImageColor.getrgb('red'))
		for r,t in self.modulation(wingen,self.config,x,y,xx,yy,shag,dic,line,popitki,False):
			dr.ellipse((r-5,h-t-5,r+5,h-t+5), fill= ImageColor.getrgb('green'))
		im.show()


	def fall(self, w, h, shag, fail ):

		line = [[0,0,w,0],[w,0,w,h],[0,0,0,h],[0,h,w,h]]
		with open(fail+'.txt', 'r') as f:
			for i,li in enumerate(f):
				a=li.replace('\n', '')
				line.append(list())
				for j in a.split(' '):
					line[i+4].append(int(j))
		dic = {}

		assert not (w%shag) and not (h%shag)
		for i in range(int(w/shag) + 1):
			for j in range(int(h/shag) + 1):
				dic[str(i) + str(j)] = set()

		for i, ii in enumerate(line):
			try:
				k = (line[i][3] - line[i][1]) / (line[i][2] - line[i][0])
				b = line[i][1] - k*line[i][0]
				t = 1
			except ZeroDivisionError:
				b = line[i][1]
				k = line[i][3] - line[i][1]
				t = 0
			#assert not k%1
			for j in range(abs(int(line[i][2] - line[i][0])) + 1):
				for n in range(int(abs(k)) + 1):
					dic[str(int((line[i][0] + j)//shag)) + str(int((k*(line[i][0] + j)*t + b +n)// shag))].add(i)
					if j == (line[i][2] - line[i][0] + 1) and k >= 0:
						break
					elif j == 0 and k < 0:
						break

		for i in range(int(w/shag) + 1):
			for j in range(int(h/shag) + 1):
				if not dic[str(i) + str(j)] :
					del dic[str(i) + str(j)]
		return dic, line


ii = Test('newconfig.ini')
w = [200]
h = [200]
x = [50]
y = [50]
xx = [150]
yy = [100]
shag = [50]
popitki = [200]
dic = []
line = []
steni = ['line1']
qwer = 10
while qwer:
	dic.clear()
	line.clear()
	for we, he, sha, lin in zip(w,h,shag,steni):
		d, l = ii.fall(we, he ,sha, lin)
		dic.append(d)
		line.append(l)

	winner = ii.p.runforest(ii.modulation, qwer,x, y, xx, yy, shag, dic, line, popitki )
	#print('\nBest genome:\n{!s}'.format(winner))

	for q in range(len(dic)):
		ii.visual(9,4,winner,w[q],h[q],x[q],y[q],xx[q],yy[q],shag[q],dic[q],line[q],popitki[q])

	qwer= int(input())
	if qwer == 2:
		qwer = 0
		with open(input(), 'wb') as fa:
			pickle.dump(winner,fa)