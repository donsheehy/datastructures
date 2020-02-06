import canvas

def draw_line(x1, y1, x2, y2):
	canvas.draw_line(x1, y1, x2, y2)
		
def draw_circle(x, y, r):
	canvas.set_line_width(3)
	canvas.set_stroke_color(0, 0, 0)
	canvas.set_fill_color(255,255,255)
	canvas.fill_ellipse(x - r, y - r, 2 * r, 2 * r)
	canvas.draw_ellipse(x - r, y - r, 2 * r, 2 * r)

def draw_label(s, x, y):
	fs = 30
	fnt = 'Helvetica-Bold'
	w, h = canvas.get_text_size(str(s), fnt, fs)
	canvas.set_fill_color(0,0,0)
	canvas.draw_text(str(s), x - w / 2, y - h / 2, fnt, fs)
