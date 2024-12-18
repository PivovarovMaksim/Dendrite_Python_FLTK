import fltk as fl
import random as rd
import os
import re
import time

FILENAME = "setting.txt" # Файл настройки

# Размеры главного окна
MAIN_WIN_W = 800
MAIN_WIN_H = 600

# Мин. и макс. размеры сторон поля
S_MIN = 50
W_MAX = MAIN_WIN_W - 10
H_MAX = MAIN_WIN_H - 40

G_MAX_PAR = 100000 # Макс. возможное кол-во частиц
G_MAX_PS = 50 # Макс. размер частицы
INDENT_WH = [5, 35] # Отступы поля

SETTING_NAMES = [
				"number_particles", "number_particles_inv", "w", "h", "particle_size", "intervals",
				"p_u", "p_d", "p_l", "p_r", "extension"
				]

SETTING_DFL = [500, 0, 300, 300, 5, "", 0.15, 0.35, 0.25, 0.25, 0] # Настройки по умолчанию
setting = [0, 0, 0, 0, 0, "", 0.0, 0.0, 0.0, 0.0, 0] # Текущие настройки

p = [0.15, 0.35, 0.25, 0.25] # Вероятности движения частицы (вверх, вниз, влево, вправо)

# Кол-во частиц (обычных и инверсных)
c_p = 0
c_pi = 0

fid_wh = [0, 0] # Размер поля
p_s = 0 # Размер частицы
inter = "" # Интервалы
fid_xy = [0, 0] # Граница поля справа и снизу
arr_xy = [] # Массив 0 и 1 для обнаружения частиц на поле
arr_init = [0] # Координаты x иниц-ции частицы
particles = [] # Частицы на поле
count = 0 # Кол-во частиц на поле
c_tol = 0 # Общее кол-во частиц
live = True # Процесс роста
net = False # Сетка
stop = True # Пауза
bid_prs = False # Процесс быстрой постройки
y_spn = 0 # Кор. y - на которой создается частица
exn = False # Расширение поля
per = 0 # Процент частиц на поле
speed = 0.015 # Скорость движения частиц
v_time = time.time() # Точка отсчета
ref = 0 # Ссылка на нужный режим моделирования
y_touch = 1000 # Кор. y касания частицы

# Класс отрисовки
class Drawing(fl.Fl_Widget):
	def draw(self):
		fl.fl_rectf(self.x(), self.y(), self.w(), self.h(), fl.FL_GRAY)
		fl.fl_rectf(INDENT_WH[0], INDENT_WH[1], fid_wh[0], fid_wh[1], fl.FL_WHITE)
		if part.type == False:
			fl.fl_rectf(part.x, part.y, p_s, p_s, fl.FL_BLACK)
		else:
			fl.fl_rectf(part.x, part.y, p_s, p_s, fl.FL_GREEN)
		for cor in particles:
			fl.fl_rectf(cor[0], cor[1], p_s, p_s, fl.FL_BLACK)
		if net and p_s > 4:
			fl.fl_color(128, 128, 128)
			for i in range(INDENT_WH[0] + p_s, fid_xy[0], p_s):
				fl.fl_line(i, INDENT_WH[1], i, fid_xy[1])
			for i in range(INDENT_WH[1] + p_s, fid_xy[1], p_s):
				fl.fl_line(INDENT_WH[0], i, fid_xy[0], i)
	
# Класс частицы
class Particle():
	def __init__(self, y, t):
		self.x = rd.choice(arr_init)
		self.y = y
		self.tch = False
		self.type = t
	
	# Движение
	def move(self):
		if self.tch == False:
			if ((arr_xy[self.y - p_s][self.x] == 1 or arr_xy[self.y + p_s][self.x] == 1 or arr_xy[self.y][self.x - p_s] == 1 or arr_xy[self.y][self.x + p_s] == 1) 
			or (self.x == INDENT_WH[0] and arr_xy[self.y][fid_xy[0] - p_s] == 1) or (self.x == fid_xy[0] and arr_xy[self.y][INDENT_WH[0]] == 1)):
				self.tch = True
				
			elif self.y < fid_xy[1] - p_s:
				r = rd.random()
				if r < p[0]:
					self.y -= p_s
					
				elif r < p[0] + p[1]:
					self.y += p_s
					
				elif r < p[0] + p[1] + p[2]:
					self.x -= p_s
					
				else:
					self.x += p_s
					 
				if self.x < INDENT_WH[0]:
					self.x = fid_xy[0] - p_s
					
				elif self.x >= fid_xy[0]:
					self.x = INDENT_WH[0] + p_s
					
			else:
				self.tch = True
			
	# Инверсия соседних частиц
	def inv(self):
		global particles, arr_xy
		if self.type == True:
			if self.tch == True and self.y != fid_xy[1] - p_s:
				mass = [[self.x, self.y - p_s], [self.x, self.y + p_s]]
				if self.x == INDENT_WH[0]:
					mass += [[fid_xy[0] - p_s, self.y], [fid_xy[0] - p_s, self.y - p_s], [fid_xy[0] - p_s, self.y + p_s]]
				else:
					mass += [[self.x - p_s, self.y], [self.x - p_s, self.y - p_s], [self.x - p_s, self.y + p_s]]
				if self.x == fid_xy[0] - p_s:
					mass += [[INDENT_WH[0], self.y], [INDENT_WH[0], self.y - p_s], [INDENT_WH[0], self.y + p_s]]
				else:
					mass += [[self.x + p_s, self.y], [self.x + p_s, self.y - p_s], [self.x + p_s, self.y + p_s]]
				for i in mass:
					if arr_xy[i[1]][i[0]] == 0 and i[1] != fid_xy[1]:
						arr_xy[i[1]][i[0]] = 1
						particles += [i]
					elif i[1] != fid_xy[1]:
						arr_xy[i[1]][i[0]] = 0
						particles.remove(i)
		 	
# Окно настроек
class Window_Setting():
	def __init__(self): 
		self.x = 180
		self.w = 450
		self.h = 300 
		self.y = 30
		self.yb = 30
		self.wi = 10
		self.hi = 20
		self.window = fl.Fl_Window(self.w, self.h, "Настройки")
		self.button = fl.Fl_Button(self.w - 110, self.h - 30, 100, 25, "Прменить")
		self.button.callback(call_set)
		self.btn_dfl = fl.Fl_Button(self.w - 110, self.h - 65, 100, 25, "По умолчанию")
		self.btn_dfl.callback(call_dfl)
		self.ipt_cp = fl.Fl_Value_Input(self.x, self.yb, self.wi * 10, self.hi, "Кол-во обычных частиц")
		self.ipt_cp.type(fl.FL_INT_INPUT)
		self.ipt_cpi = fl.Fl_Value_Input(self.x, self.yb + self.y, self.wi * 10, self.hi, "Кол-во инверсных частиц")
		self.ipt_cpi.type(fl.FL_INT_INPUT)
		self.ipt_w = fl.Fl_Value_Input(self.x, self.yb + self.y * 2, self.wi * 10, self.hi, "Ширина поля")
		self.ipt_w.type(fl.FL_INT_INPUT)
		self.ipt_h = fl.Fl_Value_Input(self.x, self.yb + self.y * 3, self.wi * 10, self.hi, "Высота поля")
		self.ipt_h.type(fl.FL_INT_INPUT)
		self.ipt_ps = fl.Fl_Value_Input(self.x, self.yb + self.y * 4, self.wi * 10, self.hi, "Размер частицы")
		self.ipt_ps.type(fl.FL_INT_INPUT)
		self.ipt_inter = fl.Fl_Input(self.x, self.yb + self.y * 5, self.wi * 23, self.hi, "Интервал")
		self.box = fl.Fl_Box(self.x * 2, self.yb, self.wi, self.hi, "Вероятности:")
		self.ipt_p_u = fl.Fl_Value_Input(self.x * 2, self.yb + self.y, self.wi * 5, self.hi, "Вверх")
		self.ipt_p_d = fl.Fl_Value_Input(self.x * 2, self.yb + self.y * 2, self.wi * 5, self.hi, "Вниз")
		self.ipt_p_l = fl.Fl_Value_Input(self.x * 2, self.yb + self.y * 3, self.wi * 5, self.hi, "Влево")
		self.ipt_p_r = fl.Fl_Value_Input(self.x * 2, self.yb + self.y * 4, self.wi * 5, self.hi, "Вправо")
		self.btn_exn = fl.Fl_Check_Button(self.x, self.yb + self.y * 6, self.wi * 11, self.hi, "Расширение")
		
# Окно помощи		
class Window_Help():
	def __init__(self):
		self.w = 800
		self.h = 600
		self.window = fl.Fl_Window(self.w, self.h, "Помощь")
		self.out = fl.Fl_Multiline_Output(5, 5, 790, 590)
		self.out.insert("Рост дендрита прекращается, если\n"
				  		"все частицы находятся на поле или высота дендрита достигла верхней границы поля;\n\n"
						"О кнопках:\n"
						"	Пуск/Пауза - запуск/остановка процесса роста дендрита;\n"
				  		"	Построить - запуск быстрой постройки дендрита;\n"
				  		"	Сетка - вкл/выкл сетки на поле (при размере частицы > 4);\n"
				  		"	Очистить - очистить консоль;\n\n"
						"О настройках:\n"
						"	Макс. значения для параметров:\n"
				  		"		Кол-во обычных и инверсных частиц - 100000;\n"
				  		"		Ширина / Высота - 790 / 560;\n"
				  		"		Размер частицы - 50;\n\n"
						"	Сумма выбранных вероятностей должна быть равна 1;\n"
				  		"	Расширение - если этот параметр активен:\n"
						"		Каждый раз, когда рост дендрита достигает верхней границы поля,\n"
						"		высота поля увеличивается.\n"
						"		Расширение перестанет работать, если высота поля достигла макс. значения (560).\n\n"
						"	Можно устанавливать определенные интервалы (по координате x),\n"
						"	в которых создаются частицы.\n\n"
						"		Интервалы вводятся по шаблону:\n"
						"			(от 1 до 3 цифр)..(от 1 до 3 цифр), (от 1 до 3 цифр)..(от 1 до 3 цифр), и т.д\n"
						"		Примеры интервалов:\n"
						"		1) 100..200\n"
						"		2) 10..20, 90..120\n\n"
						"Инверсная частица при касании модифицирует клетки вокруг себя:\n"
				  		"клетки с частицами очищаются, без - заполняются частицой")
		
# Окно "О программе"		
class Window_About():
	def __init__(self):
		self.w = 500
		self.h = 300
		self.window = fl.Fl_Window(self.w, self.h, "О программе")
		self.out = fl.Fl_Multiline_Output(5, 5, 490, 290)
		self.out.insert("Название программы: Рост дендрита\n"
				  		"Программа моделирует рост дендрита с различными параметрами\n"
						"Автор: Пивоваров М.Е.\nГруппа: 5.205-1\n"
						"Используемая графическая библиотека: FLTK\n\n"
						"2024")

# Переключение сетки
def call_net(widget):
	global net
	if net:
		net = False
	else:
		net = True
	drawing.redraw()

# Установка значений по умолчанию
def call_dfl(widget):
	window_s.ipt_cp.value(SETTING_DFL[0])
	window_s.ipt_cpi.value(SETTING_DFL[1])
	window_s.ipt_w.value(SETTING_DFL[2])
	window_s.ipt_h.value(SETTING_DFL[3])
	window_s.ipt_ps.value(SETTING_DFL[4])
	window_s.ipt_inter.value(SETTING_DFL[5])
	window_s.ipt_p_u.value(SETTING_DFL[6])
	window_s.ipt_p_d.value(SETTING_DFL[7])
	window_s.ipt_p_l.value(SETTING_DFL[8])
	window_s.ipt_p_r.value(SETTING_DFL[9])
	window_s.btn_exn.value(SETTING_DFL[10])
	
# Переключение Пуск/Пауза	
def call_stop(widget):
	global stop
	if stop == False:
		stop = True
		btn_stop.label("Пуск")
		
	else:
		stop = False
		btn_stop.label("Пауза")	

# Вызов окна настроек
def call_setting(widget):
	global live
	live = False
	window_s.window.end()
	window_s.window.show()

# Запуск быстрой постройки
def call_bid(widget):
	global stop, bid_prs, live, v_time
	per_l = int(ipt_per.value())
	if per_l < 0 or per_l > 100:
		per_l = 100
		ipt_per.value(100)
	if count < c_tol and per < per_l:
		live = True
		bid_prs = True
		stop = False
		v_time = time.time()
		btn_stop.label("Пауза")
		window_s.window.hide()
		window_a.window.hide()
		window_h.window.hide()
		main_window.hide()
		bild(per_l)
		bid_prs = False
		main_window.show()
		main_window.end()
		drawing.redraw()

# Действие кнопки "Применить"	
def call_set(widget):
	apply()
	
# Вызов окна помощи
def call_help(widget):
	window_h.window.end()
	window_h.window.show()

# Вызов окна "О программе"
def call_about(widget):
	window_a.window.end()
	window_a.window.show()

# Действия при закрытии окна
def call_hid(widget):
	global live
	if widget == window_s.window:
		if count < c_tol:
			live = True
	widget.hide()

# Завершение программы
def call_end(widget):
	global setting
	with open(FILENAME, "w") as file:
		for i in range(len(SETTING_DFL)):
			file.write(f"{SETTING_NAMES[i]} = {setting[i]}\n")	
	window_s.window.hide()
	window_a.window.hide()
	window_h.window.hide()
	main_window.hide()

# Очистка консоли	
def call_clr(widget):
	os.system('cls')

# Изменение скорости
def call_speed(widget):
	global speed
	speed = 1 / widget.value()

# Сброс скорости на значение по умолчанию	
def call_sp_res(widget):
	global speed
	speed = 0.015
	slider.value(60)

# Создание доп. окон
window_s = Window_Setting()
window_h = Window_Help()
window_a = Window_About()

# Главное окно
main_window = fl.Fl_Double_Window(MAIN_WIN_W, MAIN_WIN_H, "Рост дендрита")
main_window.callback(call_end)

# Иниц-ция частицы
part = Particle(y_spn, False)
part.tch = True

# Поле рисования
drawing = Drawing(INDENT_WH[0], INDENT_WH[1], MAIN_WIN_W, MAIN_WIN_H)

# Установка функций при закрытии окон
window_s.window.callback(call_hid)
window_a.window.callback(call_hid)
window_h.window.callback(call_hid)

# Элементы меню
menuitems = (( "&Меню", 0, 0, 0, fl.FL_SUBMENU ),
	( "&Настройки", 0, call_setting ),
	( "&Помощь", 0, call_help ),
	( "&О программе", 0, call_about ),
	( "&Выход", 0, call_end ),
	( None, 0 )
)

# Панель меню
menu_bar = fl.Fl_Menu_Bar(0, 0, 100, 30)
menu_bar.copy(menuitems)

# Кнопки
btn_stop = fl.Fl_Button(55, 0, 80, 30, "Пуск")
btn_stop.callback(call_stop)
btn_bid = fl.Fl_Button(215, 0, 80, 30, "Построить") #295
btn_bid.callback(call_bid)
btn_net = fl.Fl_Button(135, 0, 80, 30, "Сетка")
btn_net.callback(call_net)
btn_clr = fl.Fl_Button(718, 0, 80, 30, "Очистить") #135
btn_clr.callback(call_clr)
btn_sp_res = fl.Fl_Button(658, 0, 60, 30, "Сброс")
btn_sp_res.callback(call_sp_res)

# Для ввода процента быстрой постройки
ipt_per = fl.Fl_Value_Input(297, 0, 35, 30, "")
ipt_per.align(fl.FL_ALIGN_RIGHT)
ipt_per.value(100)

# Для изменения скорости частицы
slider = fl.Fl_Slider(400, 0, 257, 30, "Скорость")
slider.type(fl.FL_HORIZONTAL)
slider.color2(fl.FL_RED)
slider.align(fl.FL_ALIGN_LEFT)
slider.callback(call_speed)
slider.minimum(1)
slider.maximum(100)
slider.step(1)
slider.value(60)

# Быстрая постройка
def bild(per_l):
	while per < per_l and count < c_tol: 
		ref()

# Конец моделирования
def live_off():
	global live, count, y_touch
	if y_touch <= y_spn + p_s:
		live = False
		count = c_tol
	y_touch = 1000

# Для режима с расширением поля
def f_exn():
	global y_touch, live, count
	if fid_wh[1] + p_s <= H_MAX and y_touch <= y_spn + p_s:
		fid_wh[1] += p_s
		fid_xy[1] = INDENT_WH[1] + fid_wh[1]
		for i in particles:
			arr_xy[i[1]][i[0]] = 0
			i[1] += p_s
			arr_xy[i[1]][i[0]] = 1
	elif fid_wh[1] + p_s > H_MAX and y_touch <= y_spn + p_s:
		live = False
		count = c_tol
	y_touch = 1000

# Повтор шага моделирования
def repeat():
	if bid_prs == False:
		drawing.redraw()
		fl.Fl.repeat_timeout(speed, ref)

# Стандартный режим
def way_0():
	if stop == False and live == True:
		core()
		live_off()
	repeat()

# Режим с расширением поля
def way_1():
	if stop == False and live == True:
		core()
		f_exn()
	repeat()

# Применение настроек
def apply():
	global particles, part, c_p, c_pi, count, c_tol, arr_xy, fid_wh, p_s, arr_init, y_spn, live, v_time, inter, setting, exn, p, per, ref
	arr_xy = []
	for i in range(MAIN_WIN_H):
		l = []
		for j in range(MAIN_WIN_W):
			l.append(0)
		arr_xy.append(l)
	cp = int(window_s.ipt_cp.value())
	cpi = int(window_s.ipt_cpi.value())
	w = int(window_s.ipt_w.value())
	h = int(window_s.ipt_h.value())
	ps = int(window_s.ipt_ps.value())
	p_u = abs(window_s.ipt_p_u.value())
	p_d = abs(window_s.ipt_p_d.value())
	p_l = abs(window_s.ipt_p_l.value())
	p_r = abs(window_s.ipt_p_r.value())
	if p_u + p_d + p_l + p_r == 1:
		p = [p_u, p_d, p_l, p_r]
	else:
		p = [SETTING_DFL[6], SETTING_DFL[7], SETTING_DFL[8], SETTING_DFL[9]]
		window_s.ipt_p_u.value(SETTING_DFL[6])
		window_s.ipt_p_d.value(SETTING_DFL[7])
		window_s.ipt_p_l.value(SETTING_DFL[8])
		window_s.ipt_p_r.value(SETTING_DFL[9])
	if cp >= 0 and cp <= G_MAX_PAR:
		c_p = cp
	if cpi >= 0 and cpi <= G_MAX_PAR:
		c_pi = cpi
	if ps > 0 and ps <= G_MAX_PS:
		p_s = ps
	
	if w > W_MAX:
		window_s.ipt_w.value(W_MAX)
		fid_wh[0] = W_MAX - W_MAX % p_s
	elif w < S_MIN:
		window_s.ipt_w.value(S_MIN)
		fid_wh[0] = S_MIN - S_MIN % p_s
	else:
		fid_wh[0] = w - w % p_s
	
	if h > H_MAX:
		window_s.ipt_h.value(H_MAX)
		fid_wh[1] = H_MAX - H_MAX % p_s
	elif h < S_MIN:
		window_s.ipt_h.value(S_MIN)
		fid_wh[1] = S_MIN - S_MIN % p_s
	else:
		fid_wh[1] = h - h % p_s
	
	c_tol = c_p + c_pi
	if c_tol > G_MAX_PAR or c_tol < 1:
		c_p = SETTING_DFL[0]
		c_pi = SETTING_DFL[1]
		c_tol = c_p + c_pi
	exn = bool(window_s.btn_exn.value())
	setting[10] = window_s.btn_exn.value()
	if exn:
		ref = way_1
	else:
		ref = way_0
	window_s.ipt_cp.value(c_p)
	window_s.ipt_cpi.value(c_pi)
	window_s.ipt_ps.value(p_s)
	fid_xy[0] = INDENT_WH[0] + fid_wh[0]
	fid_xy[1] = INDENT_WH[1] + fid_wh[1]
	y_spn = INDENT_WH[1] + p_s
	
	arr_init = []
	s = window_s.ipt_inter.value()
	
	b = INDENT_WH[0]
	e = fid_xy[0]
	reg = "(\d{1,3}\.\.\d{1,3})(,\s\d{1,3}\.\.\d{1,3})*"
	
	if re.fullmatch(reg, s):
		arr = []
		s = s.split(', ')
		q = 0
		for i in s:
			arr += [i.split('..')]
			q += 1
		lgh = len(arr)
		for i in range(lgh):
			for j in range(len(arr[0])):
				arr[i][j] = int(arr[i][j])
		for i in range(lgh):
			if arr[i][0] < arr[i][1] and arr[i][1] < e:
				a = arr[i][0] + INDENT_WH[0]
				c = arr[i][1] + INDENT_WH[0]
				if a % p_s != 0:
					a -= a % p_s
					c -= c % p_s
					a += INDENT_WH[0]
					c += INDENT_WH[0]
				if c > fid_xy[0]:
					c = fid_xy[0] - fid_xy[0] % p_s
				
				for j in range(a, c, p_s):
					arr_init += [j]
		
		arr_init = set(arr_init)
		arr_init = list(arr_init)
		arr_init = sorted(arr_init)
		
	if len(arr_init) == 0:
		window_s.ipt_inter.value("")
		for i in range(b, e, p_s):
			arr_init += [i]
		
	inter = window_s.ipt_inter.value()
	
	setting[0] = c_p
	setting[1] = c_pi
	setting[2] = int(window_s.ipt_w.value())
	setting[3] = int(window_s.ipt_h.value())
	setting[4] = p_s
	setting[5] = inter
	setting[6] = p[0]
	setting[7] = p[1]
	setting[8] = p[2]
	setting[9] = p[3]
	
	particles = []
	count = 0
	per = 0
	part = Particle(y_spn, False)
	live = True
	v_time = time.time()
	window_s.window.hide()
	drawing.redraw()

# Вывод процента и времени моделирования
def prt_time(temp):
	t_sec = round(time.time() - v_time, 2)
	arr_time = [0, 0, 0]
	arr_time[0] = int(t_sec) // 60
	arr_time[1] = int(t_sec - (arr_time[0] * 60))
	arr_time[2] = int((t_sec - int(t_sec)) * 100)
	for i in range(len(arr_time)):
		arr_time[i] = str(arr_time[i])
		if len(arr_time[i]) < 2:
			arr_time[i] = '0' + arr_time[i]
	print(f"{int(temp)}% - {arr_time[0]}:{arr_time[1]}.{arr_time[2]}")
	
# Основная функция
def core():
	global count, fid_wh, particles, part, c_p, c_pi, y_spn, live, fid_xy, per, y_touch
	
	if part.tch == True:
		p_p = c_p / (c_p + c_pi)
		p_i = 1 - p_p
		r = rd.random()
		if r < p_p:
			part = Particle(y_spn, False)
			c_p -= 1
		elif r < p_p + p_i:
			part = Particle(y_spn, True)
			c_pi -= 1	
		

	if part.y < y_spn - (p_s * 10):
		part.y = y_spn
	
	part.move()
	
	if part.tch == True:
		count += 1
		particles += [[part.x, part.y]]
		arr_xy[part.y][part.x] = 1
		temp = int((count / c_tol) * 100)
		y_touch = part.y
		part.inv()
		if temp != per:
			prt_time(temp)
			per = temp
		if count == c_tol:
			live = False
		
def main():
	global c_p, c_pi, fid_wh, fid_xy, p_s, inter, c_tol, y_spn, arr_init, exn, p, setting, ref
	
	reg_inter = "(\w+\s=\s).*\s"
	reg_0 = "(\w+\s=\s)\d+\s"
	reg_1 = "(\w+\s=\s)((\d+\.\d+)|\d+)\s"
	reg_cor = f"{reg_inter}|{reg_0}|{reg_1}"
	
	if os.path.exists("setting.txt"):
		with open(FILENAME, "r") as file:
			j = 0
			for line in file:
				#print(list(line))
				if re.fullmatch(reg_cor, line):
					s = line.split("\n")
					s = s[0].split(" = ")
					if (re.fullmatch(reg_0, line) and j in (0, 1, 2, 3, 4, 10)) \
						or (re.fullmatch(reg_1, line) and j in (6, 7, 8, 9)) \
						or j == 5:
						#print(f"{j} - yes")
						setting[j] = type(SETTING_DFL[j])(s[1])
						j += 1
					else:
						print(f"Ошибка в формате данных в настройках: строка {j + 1}")
						return 0
				else:
					print(f"Ошибка в структуре файла настроек: строка {j + 1}")
					return 0
	else:
		with open(FILENAME, "w") as file:
			for i in range(len(SETTING_DFL)):
				file.write(f"{SETTING_NAMES[i]} = {SETTING_DFL[i]}\n")
		setting = SETTING_DFL
	
	window_s.ipt_cp.value(setting[0])
	window_s.ipt_cpi.value(setting[1])
	window_s.ipt_w.value(setting[2])
	window_s.ipt_h.value(setting[3])
	window_s.ipt_ps.value(setting[4])
	window_s.ipt_inter.value(setting[5])
	window_s.ipt_p_u.value(setting[6])
	window_s.ipt_p_d.value(setting[7])
	window_s.ipt_p_l.value(setting[8])
	window_s.ipt_p_r.value(setting[9])
	window_s.btn_exn.value(setting[10])

	apply()
	ref()

	main_window.show()
	main_window.end()

	fl.Fl.run()
main()	


