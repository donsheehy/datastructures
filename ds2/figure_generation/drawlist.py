from ds_viz.gizehcanvas import Canvas
from ds_viz.vizsequence import drawlist as drawtocanvas

def drawlist(L, name):
    canvas = Canvas(700, 60)
    drawtocanvas(L, (10,10), canvas)
    canvas.surface.write_to_png('figures/' + name + '.png')
