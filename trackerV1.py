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

	def chek(self, i, x, y, dic):

		vector = [1, 1, -1, -1]
		if i == 0 or i == 2:
			y += vector[i]
		else:
			x += vector[i]
		return dic.get(str(x)+'x'+str(y),0)

	def modulation(self, genome, config, x, y, xx, yy,
					dic, popitki, regim=True):

		dark = []
		ty = neat.nn. FeedForwardNetwork.create(genome, config)
		new = 0
		daun = -10000
		for l in range(popitki):
			#НОВИЗНА МЕСТА
			povtor = dark.count([x,y])
			#КОЛИЧЕСТВО НЕПОВТОРЯЕМЫХ КООРДИНАТ(путь)
			if povtor == 0:
				new += 1
			#ОГРАНИЧИВАНИЕ ПОВТОРЕНИЙ
			if povtor > 2:
				break
			dark.append([x,y])
			net = True
			try:
				k = (yy-y)/(xx-x)
				b = y - k*x
				for i in range(min(x,xx), max(x,xx)+1):
					if dic.get(str(i)+'x'+str(int(k*i+b))) ==1:
						net = False
						v = [0,0,0,0]
						break
			except ZeroDivisionError:
				for i in range(min(y,yy), max(y,yy)+1):
					if dic.get(str(x)+'x'+str(i)) == 1:
						net = False
						v = [0,0,0,0]	
			if net:
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
				v.append(self.chek(i, x, y, dic))
			v.append(10*povtor**2)

			move = ty.activate(v)
			best = move.index(max(move))
			
			if v[4 + best] == 1:
				continue
			if best == 1:
				x += 1
			elif best == 0:
				y += 1
			elif best == 3:
				x -= 1
			elif best == 2:
				y -= 1
			if x == xx and y == yy:
				daun = 0
				break
		if regim:
			return daun + new
		else:
			return dark

	def visual(self, vhod,vihod,wingen,w,h,x,y,xx,yy,dic,mn,popitki):

		vh = [i for i in range(-1,-vhod-1,-1)]
		vh.extend([i for i in range(vihod)])
		node_names = {x:str(x) for x in vh}
		#visualize.draw_net(self.config, wingen, True, node_names=node_names, fmt='png')
		#visualize.plot_stats(self.stats, ylog=False, view=True)
		#visualize.plot_species(self.stats, view=True)
		im = Image.new('RGB', (mn*(w),mn*(h)),(0,0,0))
		dr = ImageDraw.Draw(im)
		dr.rectangle((mn*(x-0.5),mn*(h-y-0.5),mn*(x+0.5),mn*(h-y+0.5)), fill=ImageColor.getrgb('red'))
		dr.rectangle((mn*(xx-0.5),mn*(h-yy-0.5),mn*(xx+0.5),mn*(h-yy+0.5)), fill=ImageColor.getrgb('blue'))
		for i in dic.keys():
			ox,oy = i.split('x')
			dr.rectangle((mn*(int(ox)-0.5),mn*(h-int(oy)-0.5), mn*(int(ox)+0.5),mn*(h-int(oy)+0.5)), fill=ImageColor.getrgb('red'))
		for r,t in self.modulation(wingen,self.config,x,y,xx,yy,dic,popitki,False):
			dr.ellipse((mn*(r-0.5),mn*(h-t-0.5),mn*(r+0.5),mn*(h-t+0.5)), fill= ImageColor.getrgb('green'))
		im.show()

	def fall(self, fail):

		pic = Image.open(fail+'.png')
		pix = pic.load()
		dic = {}
		for i in range(pic.size[0]):
			for j in range(pic.size[1]):
				if pix[i,j] == 0:
					dic[str(i)+'x'+str(pic.size[1]-1-j)] = 1
		return dic, pic.size[0], pic.size[1]


ii = Test('newconfig.ini')
w = []
h = []
x = [10,10]
y = [3,3]
xx = [10,10]
yy = [16,16]
popitki = [200,200]
dic = []
steni = ['pic','pic2']
qwer = 10

while qwer:
	dic.clear()
	w.clear()
	h.clear()

	for we in steni:
		d, l, m = ii.fall(we)
		dic.append(d)
		w.append(l)
		h.append(m)

	winner = ii.p.runforest(ii.modulation, qwer,x, y, xx, yy, dic, popitki )
	#print('\nBest genome:\n{!s}'.format(winner))

	for q in range(len(x)):
		ii.visual(9,4,winner,w[q],h[q],x[q],y[q],xx[q],yy[q],dic[q],30,popitki[q])

	qwer= int(input())
	if qwer == 2:
		qwer = 0
		with open(input(), 'wb') as fa:
			pickle.dump(winner,fa)