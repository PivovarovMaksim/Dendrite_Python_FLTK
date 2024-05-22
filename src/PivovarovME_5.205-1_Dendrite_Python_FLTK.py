from fltk import *
from random import *
import time
import sys
import os
from re import *

fid_xy = [300, 300]
tfid_xy = [10, 40]
p_s = 10
clear = lambda: os.system('cls')

m_xy = []
for i in range(600):
	l = []
	for j in range(800):
		l.append(0)
	m_xy.append(l)
	
'''for i in range(800):
	m_xy[fid_xy[1]][i] = 2'''
	
'''for i in range(fid_xy[1]+1):
	for j in range(fid_xy[0]):
		if j == 0:
			print()
		print(m_xy[i][j], end='')'''	

class Drawing(Fl_Widget):
	def draw(self):
		global count, particles, part, c_p, c_pi, t_p, c_max, tfid_xy, p_s, fid_xy
		#fl_rectf(self.x(), self.y(), self.w(), self.h(), FL_WHITE)
		fl_rectf(self.x(), self.y(), self.w(), self.h(), FL_GRAY)
		#print("Create")
		fl_rectf(tfid_xy[0], tfid_xy[1], fid_xy[0], fid_xy[1], FL_WHITE)
		if count < c_max:
			if t_p == False:
				fl_rectf(part.x, part.y, p_s, p_s, FL_BLACK)
			else:
				fl_rectf(part.x, part.y, p_s, p_s, FL_GREEN)
		
		for cor in particles:
			fl_rectf(cor[0], cor[1], p_s, p_s, FL_BLACK)
		
		'''for cor in particles_d:
			fl_rectf(cor[0], cor[1], p_s, p_s, FL_RED)
		
		for cor in particles_g:
			fl_rectf(cor[0], cor[1], p_s, p_s, FL_GREEN)
		
		for cor in particles_a:
			fl_rectf(cor[0], cor[1], p_s, p_s, FL_BLUE)'''
		
		
			
	
class Particle():
	def __init__(self, y):
		self.x = choice(m_rand)
		self.y = y
		self.t = False
	def move(self):
		global particles, p_s, fid_xy, tfid_xy
		
		if m_xy[self.y-p_s][self.x] == 1 or m_xy[self.y+p_s][self.x] == 1 or m_xy[self.y][self.x-p_s] == 1 or m_xy[self.y][self.x+p_s] == 1:
			self.t = True
			
		if self.y < fid_xy[1] + tfid_xy[1] - p_s and self.t == False:
			r = random()
			if r < p[0]:
				self.y -= p_s
				
			elif r < p[0]+p[1]:
				self.x -= p_s
				
			elif r < p[0]+p[1]+p[2]:
				self.x += p_s
				
			else:
				self.y += p_s
				 
			if self.x <= tfid_xy[0]:
				self.x = tfid_xy[0]+fid_xy[0]-p_s
				
			if self.x >= tfid_xy[0]+fid_xy[0]:
				self.x = tfid_xy[0]+p_s
				
		else:
			self.t = True
			
class Particle_I():
	def __init__(self, y):
		self.x = choice(m_rand)
		self.y = y
		self.t = False
	def move(self):
		global particles, p_s, fid_xy, tfid_xy, particles_g, particles_d, particles_a
		
		if m_xy[self.y-p_s][self.x] == 1 or m_xy[self.y+p_s][self.x] == 1 or m_xy[self.y][self.x-p_s] == 1 or m_xy[self.y][self.x+p_s] == 1:
			self.t = True
			
			mass = [[self.x-p_s, self.y-p_s], [self.x-p_s, self.y], [self.x-p_s, self.y+p_s], [self.x, self.y-p_s], [self.x, self.y+p_s], [self.x+p_s, self.y-p_s], [self.x+p_s, self.y], [self.x+p_s, self.y+p_s]] 
			print(self.x, self.y)
			for i in mass:
				print(i)
				print(m_xy[i[1]][i[0]])
				if m_xy[i[1]][i[0]] == 0:
					 m_xy[i[1]][i[0]] = 1
					 #particles_a += [i]
					 particles += [i]
				else:
					m_xy[i[1]][i[0]] = 0
					particles.remove(i)
					#particles_d += [i]
					
				
			
		if self.y < fid_xy[1] + tfid_xy[1] - p_s and self.t == False:
			r = random()
			if r < p[0]:
				self.y -= p_s
				
			elif r < p[0]+p[1]:
				self.x -= p_s
				
			elif r < p[0]+p[1]+p[2]:
				self.x += p_s
				
			else:
				self.y += p_s
				
			if self.x <= tfid_xy[0]:
				self.x = tfid_xy[0]+fid_xy[0]-p_s
				
			if self.x >= tfid_xy[0]+fid_xy[0]:
				self.x = tfid_xy[0]+p_s
				
		else:
			self.t = True
			
		'''if self.t == True:
			particles_g += [[self.x, self.y]]'''
			
		 	
class Window_Setting():
	def __init__(self): 
		self.x = 180
		self.w = 400
		self.h = 300 
		self.y = 40
		self.yb = 30
		self.wi = 100
		self.hi = 20
		self.window = Fl_Window(self.w, self.h, "Настройки")
		self.button = Fl_Button(self.w-100, self.h-30, 90, 25, "Прменить")
		self.button.callback(call_set)
		self.ipt_cp = Fl_Value_Input(self.x, self.yb, self.wi, self.hi, "Кол-во обычных частиц")
		self.ipt_cp.type(FL_INT_INPUT)
		self.ipt_cpi = Fl_Value_Input(self.x, self.yb+self.y, self.wi, self.hi, "Кол-во инверсных частиц")
		self.ipt_cpi.type(FL_INT_INPUT)
		self.ipt_w = Fl_Value_Input(self.x, self.yb+self.y*2, self.wi, self.hi, "Ширина поля")
		self.ipt_w.type(FL_INT_INPUT)
		self.ipt_h = Fl_Value_Input(self.x, self.yb+self.y*3, self.wi, self.hi, "Высота поля")
		self.ipt_h.type(FL_INT_INPUT)
		self.ipt_ps = Fl_Value_Input(self.x, self.yb+self.y*4, self.wi, self.hi, "Размер частицы")
		self.ipt_ps.type(FL_INT_INPUT)
	
		
	

def call_stop(widget):
	global stop
	if stop == False:
		stop = True
	else:
		stop = False		

def call_setting(widget):
	global window_s, end
	window_s.window.end()
	window_s.window.show()
	end = True
	print(end)
	
def call_set(widget):
	global particles, t_p, part, c_p, c_pi, count, c_max, window_s, m_xy, fid_xy, p_s, drawing, tfid_xy, end
	m_xy = []
	for i in range(600):
		l = []
		for j in range(800):
			l.append(0)
		m_xy.append(l)
	c_p = int(window_s.ipt_cp.value())
	c_pi = int(window_s.ipt_cpi.value())
	fid_xy[0] = int(window_s.ipt_w.value())
	fid_xy[1] = int(window_s.ipt_h.value())
	p_s = int(window_s.ipt_ps.value())
	
	particles = []
	count = 0
	c_max = c_p + c_pi
	t_p = False
	part = Particle(90)
	end = False
	print(end)
	main()
	window_s.window.hide()
	
	
	

m_rand = []
for i in range(tfid_xy[0], tfid_xy[0]+fid_xy[0], p_s):
	m_rand += [i]
	
window_s = Window_Setting()

main_window = Fl_Double_Window(800, 600, "Дендрит")




#drawing = Drawing(tfid_xy[0], tfid_xy[1], fid_xy[0], fid_xy[1])
drawing = Drawing(tfid_xy[0], tfid_xy[1], 800, 600)

menuitems = (( "&Меню", 0, 0, 0, FL_SUBMENU ),

	( "&Настройки", 0, call_setting ),
    

	( "&Помощь", 0, 0, 0, FL_MENU_DIVIDER ),
    

	( "&О программе", 0, 0, 0, FL_MENU_DIVIDER ),
    

  ( None, 0 )
)

menu_bar = Fl_Menu_Bar(0, 0, 800, 30)
menu_bar.copy(menuitems)


button_stop = Fl_Button(55, 0, 70, 30, "Стоп")
button_stop.callback(call_stop)



particles = []
particles_d = []
particles_g = []
particles_a = []
count = 0
c_p = 100
c_pi = 50
c_max = c_p+c_pi
end = False
stop = False
part = Particle(90)
t_p = False

p = [0.05, 0.22, 0.23, 0.5]
	
def main():
	global drawing, count, fid_xy, tfid_xy, particles, p_s, flag, part, c_p, c_pi, t_p, stop, end
	
	#while count < c_max:
	if stop == False:
		if (count == 0 or part.t == True) and count < c_max and (c_p > 0 or c_pi > 0):
			#clear()
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
			#fid_xy[1] += 5
			particles += [[part.x, part.y]]
			m_xy[part.y][part.x] = 1
			#print([part.x, part.y])
		
		drawing.redraw()
	if end == False:
		#print("раб")
		Fl.repeat_timeout(0.015, main)

main()

main_window.end()
main_window.show()



Fl.run()
		
