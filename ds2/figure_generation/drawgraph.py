import canvas
from drawing import draw_line, draw_circle, draw_label
#from graph import Graph

scale = 80
radius = 23
pos = [(1,1), (3,1), (1,3), (4,2), (4,6), (2,4), (1,6)]
pos = [(a * scale, b * scale) for a,b in pos]

def setstyle(w, gray = 0):
	canvas.set_line_width(w)
	canvas.set_stroke_color(gray,gray, gray)

def drawedge(u, v, w = False):
	w = w or ""
	x1, y1 = pos[u]
	x2, y2 = pos[v]
	draw_line(x1, y1, x2, y2)
	x,y = (x1 + x2) / 2 + 10, (y1 + y2) / 2 + 10
	draw_label(str(w), x, y)
	

def drawvertex(v):
	a,b = pos[v]
	draw_circle(a, b, radius)
	draw_label(str(v), a, b)

def draw(G, w = 4, g = 0):
	if isinstance(G, dict):
		G = dicttograph(G)
	setstyle(w, g)
	for e in G.edges():
		drawedge(*e)
	for v in G.vertices():
		drawvertex(v)
		
def clear():
	canvas.clear()
