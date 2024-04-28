from fltk import *
from random import *
import time
import sys

fid_xy = [750, 550]
tfid_xy = [10, 40]
p_s = 5

m_xy = []
for i in range(600):
	l = []
	for j in range(800):
		l.append(0)
	m_xy.append(l)
	
for i in range(800):
	m_xy[fid_xy[1]][i] = 2
	
'''for i in range(fid_xy[1]+1):
	for j in range(fid_xy[0]):
		if j == 0:
			print()
		print(m_xy[i][j], end='')'''	

class Drawing(Fl_Widget):
	def draw(self):
		global x, y, count, particles, part, c_p, c_pi, t_p, c_max
		fl_rectf(self.x(), self.y(), self.w(), self.h(), FL_GRAY)
		fl_rectf(tfid_xy[0], tfid_xy[1], fid_xy[0], fid_xy[1], FL_WHITE)
		if count <= c_max:
			if t_p == False:
				fl_rectf(part.x, part.y, p_s, p_s, FL_BLACK)
			else:
				fl_rectf(part.x, part.y, p_s, p_s, FL_GREEN)
		for cor in particles:
			fl_rectf(cor[0], cor[1], p_s, p_s, FL_BLACK)
			
	
class Particle():
	def __init__(self, y):
		self.x = choice(m_rand)
		self.y = y
		self.x_m = self.x - tfid_xy[0]
		self.y_m = self.y - tfid_xy[1]
		self.t = False
	def move(self):
		global particles, p_s, fid_xy, tfid_xy
		'''for i in particles:
			if (self.x == i[0] and self.y == i[1] - p_s) or (self.x == i[0] - p_s and self.y == i[1]) or (self.x == i[0] + p_s and self.y == i[1]) or (self.x == i[0] and self.y == i[1]+p_s):
				self.t = True
				break'''
		if m_xy[self.y_m-p_s][self.x_m] == 1 or m_xy[self.y_m+p_s][self.x_m] == 1 or m_xy[self.y_m][self.x_m-p_s] == 1 or m_xy[self.y_m][self.x_m+p_s] == 1:
			self.t = True
		if self.y < fid_xy[1] + tfid_xy[1] - p_s and self.t == False:
			r = random()
			if r < p[0]:
				self.y -= p_s
				self.y_m -= p_s 
			elif r < p[0]+p[1]:
				self.x -= p_s
				self.x_m -= p_s
			elif r < p[0]+p[1]+p[2]:
				self.x += p_s
				self.x_m += p_s
			else:
				self.y += p_s
				self.y_m += p_s 
			if self.x <= tfid_xy[0]:
				self.x = tfid_xy[0]+fid_xy[0]-p_s
				self.x_m = fid_xy[0]-p_s
			if self.x >= tfid_xy[0]+fid_xy[0]:
				self.x = tfid_xy[0]+p_s
				self.x_m = p_s 
		else:
			self.t = True
			
class Particle_I():
	def __init__(self, y):
		self.x = choice(m_rand)
		self.y = y
		self.x_m = self.x - tfid_xy[0]
		self.y_m = self.y - tfid_xy[1]
		self.t = False
	def move(self):
		global particles, p_s, fid_xy, tfid_xy
		for i in particles:
			if (self.x == i[0] and self.y == i[1] - p_s) or (self.x == i[0] - p_s and self.y == i[1]) or (self.x == i[0] + p_s and self.y == i[1]) or (self.x == i[0] and self.y == i[1]+p_s):
				self.t = True
				mass = [[self.x-p_s, self.y-p_s], [self.x-p_s, self.y], [self.x-p_s, self.y+p_s], [self.x, self.y-p_s], [self.x, self.y+p_s], [self.x+p_s, self.y-p_s], [self.x+p_s, self.y], [self.x+p_s, self.y+p_s]] 
				particles_1 = particles
				for j in mass:
					q = False
					for k in particles:
						if j == k:
							q = True
							break
					if q == True:
						particles_1.remove(j)
					else:
						particles_1 += [j]
				particles = particles_1	 
				break
		if self.y < fid_xy[1] + tfid_xy[1] - p_s and self.t == False:
			r = random()
			if r < p[0]:
				self.y -= p_s
				self.y_m -= p_s 
			elif r < p[0]+p[1]:
				self.x -= p_s
				self.x_m -= p_s
			elif r < p[0]+p[1]+p[2]:
				self.x += p_s
				self.x_m += p_s
			else:
				self.y += p_s
				self.y_m += p_s 
			if self.x <= tfid_xy[0]:
				self.x = tfid_xy[0]+fid_xy[0]-p_s
				self.x_m = fid_xy[0]-p_s
			if self.x >= tfid_xy[0]+fid_xy[0]:
				self.x = tfid_xy[0]+p_s
				self.x_m = p_s 
		else:
			self.t = True
			
		 	
def call_stop(widget):
	global stop
	if stop == False:
		stop = True
	else:
		stop = False		


m_rand = []
for i in range(tfid_xy[0], tfid_xy[0]+fid_xy[0], p_s):
	m_rand += [i]
window = Fl_Window(800, 600, "title")
drawing = Drawing(10, 40, 700, 500)

menuitems = (( "&Настройки", 0, 0, 0, FL_MENU_DIVIDER ),
    

  ( "&Помощь", 0, 0, 0, FL_MENU_DIVIDER ),
    

  ( "&О программе", 0, 0, 0, FL_MENU_DIVIDER ),
    

  ( None, 0 )
)




	


menu_bar = Fl_Menu_Bar(0, 0, 800, 30)
menu_bar.copy(menuitems)



button_stop = Fl_Button(260, 0, 70, 30, "stop")
button_stop.callback(call_stop)



particles = []
count = 0
c_p = 1000
c_pi = 0
c_max = c_p+c_pi
flag = False
end = False
stop = False
x = 0
y = 0
part = Particle(90)
t_p = False

p = [0.05, 0.22, 0.23, 0.5]

'''def main():
	global x, y, drawing, count, fid_xy, tfid_xy, particles, flag, p_s, end
	
	if count == 0:
		flag = True
	if flag == True and count <= c_max:
		x = choice([30, 40, 50, 80, 120])
		y = 90
		flag = False
		count += 1
	if y < fid_xy[1] + tfid_xy[1] - p_s and flag == False:
		r = random()
		if r < p_l:
			x -= p_s
		elif r < p_l + p_r:
			x += p_s
		elif r < p_l + p_r + p_d:
			y += p_s
		else:
			y -= p_s
		for p in particles:
			if (x == p[0] and y == p[1] - p_s) or (x == p[0] - p_s and y == p[1]) or (x == p[0] + p_s and y == p[1]):
				flag = True
				
	if y >= fid_xy[1] + tfid_xy[1] - p_s or flag == True:
		particles += [[x, y]]
		print(particles)
		flag = True
		
	drawing.redraw()
	Fl.repeat_timeout(0.015, main)'''
	
def main():
	global drawing, count, fid_xy, tfid_xy, particles, p_s, flag, part, c_p, c_pi, t_p, stop
	
	while count < c_max:
		if stop == False:
			if (count == 0 or part.t == True) and count < c_max and (c_p > 0 or c_pi > 0):
				print(c_p)
				p_p = c_p/(c_p+c_pi)
				p_i = 1-p_p
				r = random()
				#print(r)
				#print(p_p)
				if r < p_p and c_p > 0:
					#print(1)
					part = Particle(90)
					t_p = False
					c_p -= 1
				elif r < p_p + p_i and c_pi > 0:
					#print(0)
					part = Particle_I(90)
					t_p = True
					c_pi -= 1	
				count += 1
			if part.t == False:
				part.move()
				#print(part.y)
			if part.t == True:
				particles += [[part.x, part.y]]
				m_xy[part.y_m][part.x_m] = 1
				#print([part.x, part.y])
		
	drawing.redraw()
	#Fl.repeat_timeout(0.025, main)

main()

window.end()
window.show()

Fl.run()
		
