from PIL import Image, ImageDraw
from random import randint
from math import sin, cos, inf, sqrt, pi


# =================================== CONFIG ===================================
INPUT_WALL_COLOR = (0, 0, 0)
INPUT_VIEWER_COLOR = (0, 255, 0)
OUTPUT_TILE_SIZE = 16
OUTPUT_EDGE_WIDTH = 2
OUTPUT_VERTEX_SIZE = 2
RAY_SPACING = 2
RAY_LENGTH = 1000
RAY_WIDTH = 1


# =================================== TOOLS ===================================
class Edge:
	def __init__(self, xs, ys, xe, ye):
		self.xs: float = xs
		self.ys: float = ys
		self.xe: float = xe
		self.ye: float = ye
		
	def show(self):
		print(f'xs: {self.xs}, ys: {self.ys}, xe: {self.xe}, ye: {self.ye}')

class Tile:
	def __init__(self, value):
		self.value: bool = value
		self.edge_left: Edge = None
		self.edge_top: Edge = None
		self.edge_right: Edge = None
		self.edge_bottom: Edge = None
	
def edge_length(x1, y1, x2, y2):
	return sqrt((x1 - x2)**2 + (y1 - y2)**2)
	
# =================================== IN ===================================
image_in = Image.open('in.png')
width, height = image_in.size
pixels = image_in.load()


# =================================== CALCULATE ===================================
tiles = []
edges = []
viewers = []

for x in range(width):
	row = []
	for y in range(height):
		if pixels[x, y][0:3] == INPUT_WALL_COLOR:
			row.append(Tile(True))
		elif pixels[x, y][0:3] == INPUT_VIEWER_COLOR:
			row.append(Tile(False))
			viewers.append((x, y))
		else:
			row.append(Tile(False))
	tiles.append(row)

for y in range(height):
	for x in range(width):
	
		t = tiles[x][y]
		
		# tile is a wall ?
		if t.value:
			
			# no left neighbour ?
			if not (x == 0 or tiles[x-1][y].value):
			
				# top has edge to extend ?
				if y != 0 and tiles[x][y-1].edge_left is not None:
					n_edge = tiles[x][y-1].edge_left
					n_edge.xe = x - 0.5
					n_edge.ye = y + 0.5
					t.edge_left = n_edge
				else :
					t.edge_left = Edge(x - 0.5, y - 0.5, x - 0.5, y + 0.5)
					edges.append(t.edge_left)
					
				
			# no top neighbour ?
			if not (y == 0 or tiles[x][y-1].value):
			
				# left has edge to extend ?
				if y != 0 and tiles[x-1][y].edge_top is not None:
					n_edge = tiles[x-1][y].edge_top
					n_edge.xe = x + 0.5
					n_edge.ye = y - 0.5
					t.edge_top = n_edge
				else :
					t.edge_top = Edge(x - 0.5, y - 0.5, x + 0.5, y - 0.5)
					edges.append(t.edge_top)

	
			# no right neighbour ?
			if not (x == width - 1 or tiles[x+1][y].value):
			
				# top has edge to extend ?
				if y != 0 and tiles[x][y-1].edge_right is not None:
					n_edge = tiles[x][y-1].edge_right
					n_edge.xe = x + 0.5
					n_edge.ye = y + 0.5
					t.edge_right = n_edge
				else :
					t.edge_right = Edge(x + 0.5, y - 0.5, x + 0.5, y + 0.5)
					edges.append(t.edge_right)
				
			# no bottom neighbour ?
			if not (y == height - 1 or tiles[x][y+1].value):
			
				# left has edge to extend ?
				if y != 0 and tiles[x-1][y].edge_bottom is not None:
					n_edge = tiles[x-1][y].edge_bottom
					n_edge.xe = x + 0.5
					n_edge.ye = y + 0.5
					t.edge_bottom = n_edge
				else :
					t.edge_bottom = Edge(x - 0.5, y + 0.5, x + 0.5, y + 0.5)
					edges.append(t.edge_bottom)
					
	
# =================================== OUT ===================================
image_out = Image.new('RGB', (width * OUTPUT_TILE_SIZE, height * OUTPUT_TILE_SIZE), (255, 255, 255))
image_out_draw = ImageDraw.Draw(image_out)
	
for x in range(width):
	for y in range(height):
		if tiles[x][y].value:
			x0 = x * OUTPUT_TILE_SIZE
			y0 = y * OUTPUT_TILE_SIZE
			x1 = x0 + OUTPUT_TILE_SIZE
			y1 = y0 + OUTPUT_TILE_SIZE
			image_out_draw.rectangle([x0, y0, x1, y1],  fill=INPUT_WALL_COLOR)
			
for e in edges:
	xs = e.xs * OUTPUT_TILE_SIZE + OUTPUT_TILE_SIZE/2
	ys = e.ys * OUTPUT_TILE_SIZE + OUTPUT_TILE_SIZE/2
	xe = e.xe * OUTPUT_TILE_SIZE + OUTPUT_TILE_SIZE/2
	ye = e.ye * OUTPUT_TILE_SIZE + OUTPUT_TILE_SIZE/2
	image_out_draw.line([xs, ys, xe, ye], fill=(255, 0, 0), width=OUTPUT_EDGE_WIDTH)
	image_out_draw.ellipse([xs - OUTPUT_VERTEX_SIZE, ys - OUTPUT_VERTEX_SIZE, 
							xs + OUTPUT_VERTEX_SIZE, ys + OUTPUT_VERTEX_SIZE],
							fill=(0, 0, 255))
	image_out_draw.ellipse([xe - OUTPUT_VERTEX_SIZE, ye - OUTPUT_VERTEX_SIZE, 
							xe + OUTPUT_VERTEX_SIZE, ye + OUTPUT_VERTEX_SIZE],
							fill=(0, 0, 255))


image_out.save(f'out.png')


# =================================== OUT - RAYS ===================================
image_out = Image.new('RGB', (width * OUTPUT_TILE_SIZE, height * OUTPUT_TILE_SIZE), (0, 0, 0))
image_out_draw = ImageDraw.Draw(image_out)
	
for x in range(width):
	for y in range(height):
		if tiles[x][y].value:
			x0 = x * OUTPUT_TILE_SIZE
			y0 = y * OUTPUT_TILE_SIZE
			x1 = x0 + OUTPUT_TILE_SIZE
			y1 = y0 + OUTPUT_TILE_SIZE
			image_out_draw.rectangle([x0, y0, x1, y1],  fill=(255, 0, 0))
			
for v in viewers:
	color = (randint(0, 255), randint(0, 255), randint(0, 255))
	x0 = v[0] * OUTPUT_TILE_SIZE - OUTPUT_TILE_SIZE/2
	y0 = v[1] * OUTPUT_TILE_SIZE - OUTPUT_TILE_SIZE/2
	x1 = x0 + OUTPUT_TILE_SIZE
	y1 = y0 + OUTPUT_TILE_SIZE
	image_out_draw.rectangle([x0, y0, x1, y1],  fill=color)
	
	for d in range(0, 360, RAY_SPACING):
	
		# ray endpoints
		x3 = v[0]
		y3 = v[1]
		x4 = v[0] + RAY_LENGTH * cos(pi * d/180)
		y4 = v[1] + RAY_LENGTH * sin(pi * d/180)
		
		# checking collisions with edges
		for edge in edges:
			x1 = edge.xs
			y1 = edge.ys
			x2 = edge.xe
			y2 = edge.ye
			
			t_nom = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
			u_nom = - ((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3))
			t_den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4) # if 0 -> lines parallel
			
			if t_den == 0:
				continue
			
			t = t_nom/t_den
			u = u_nom/t_den
			
			
			# not within the edges range or wrong side of the ray
			if not 0 < t < 1 or not 0 < u: 
				continue
				
			else:
				x_cross = x1 + t * (x2 - x1)
				y_cross = y1 + t * (y2 - y1)
				
				# is the clipped ray shorter ?
				if edge_length(x3, y3, x4, y4) > edge_length(x3, y3, x_cross, y_cross):
					x4 = x_cross
					y4 = y_cross
				
			
		xs = x3 * OUTPUT_TILE_SIZE
		ys = y3 * OUTPUT_TILE_SIZE
		xe = x4 * OUTPUT_TILE_SIZE + OUTPUT_TILE_SIZE/2
		ye = y4 * OUTPUT_TILE_SIZE + OUTPUT_TILE_SIZE/2
		
		image_out_draw.line([xs, ys, xe, ye], fill=color, width=RAY_WIDTH)
	

image_out.save(f'out-rays.png')
			
			