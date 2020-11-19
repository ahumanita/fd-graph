from tkinter import *
from random import random
from graph import Node, Edge, Graph
from time import sleep
import records
from math import sqrt
from copy import deepcopy

db = records.Database(open("connection.txt","r").read().split()[0])

def get_number_of_areas() :
    number_a = db.query("SELECT max(area.id) FROM area")[0]["max"]
    return number_a
    
def get_number_of_paths() :
    number_p = db.query("SELECT max(path.id) FROM path")[0]["max"]
    return number_p

#pl: place, num_i: number of items, it#?: item, cr: creatures
def get_areas(V) :
    number_a = get_number_of_areas()
    i = 1
    area_list = []
    #collect information for tikz-field
    while i <= number_a :
        act_area = {}
        place = db.query("""SELECT area.name, area.id, area.light, area.directions_complete, area.items, 
        				area.treasure, area.information, area.creatures FROM area WHERE area.id = :id""",
        				id=i)
        place.all()
       	for key in place[0].keys() :
       		act_area[key] = place[0][key]
        area_list.append(act_area)
        
        V.append(Node(i))
        i += 1
    return area_list

#p_id: path id, st: start, des: destination, num_d: number of directions, d#: direction, col: color
#TODO keys anzeigen (ort)
def get_paths(V,E,edge_count) :
	number_p = get_number_of_paths()
	path_list = []

	i = 1
	while i <= number_p :
		act_path = {}
		color = ""
		path = db.query("""SELECT path.id, path.start, path.destination, path.direction,
			path.usable, path.information, path.waterpath, path.notes
			FROM path
			WHERE path.id = :p_id
			AND path.destination IS NOT NULL"""
			, p_id = i)
		path.all()

		if not path :
			pass
			# path = db.query("""SELECT  path.id, path.start, path.destination, path.direction,
			# 	path.usable, path.information, path.waterpath, path.notes FROM path WHERE path.id = :p_id"""
			# 	, p_id = i)
			# for key in path[0].keys() :
			# 	if key == "destination" :
			# 		act_path[key] = "NON%d" %(i)
			# 		V.append(Node("NON%d" %(i)))
			# 	else :
			# 		act_path[key] = path[0][key]
			# E.append(Edge(i,int(path[0]["start"]),"NON%d" %(i),dir=path[0]["direction"]))
			# edge_count[(int(path[0]["start"]),"NON%d" %(i))] = 1

		else :
			for key in path[0].keys() :
				act_path[key] = path[0][key]
			E.append(Edge(i,int(path[0]["start"]),int(path[0]["destination"]),dir=path[0]["direction"]))
			edge_count[(int(path[0]["start"]),int(path[0]["destination"]))] += 1
		path_list.append(act_path)

		i += 1
	return path_list


# assert random coordinates to nodes of graph between 0 and 1
def random_coords(V,width,height) :
	for node in V :
		t_w = random()
		t_h = random()
		node.x = (width*t_w,height*t_h)

# place nodes according to the coordinates as ovals in canvas
def draw_nodes(w,V,arc_rad,w_width,w_height,scaling) :
	for node in V :
		w.create_oval(int(scaling*node.x[0]+arc_rad)
			,int(scaling*node.x[1]+arc_rad)
			,int(scaling*node.x[0]-arc_rad)
			,int(scaling*node.x[1]-arc_rad)
			,fill="blue")

# always compute the curve node on the left side of the arrow when looking to its direction
# inline? 
def get_edge_curve_node(start,target,DIST) :
	mid = (start[0]+1/2*(target[0]-start[0]),start[1]+1/2*(target[1]-start[1]))

	# turn the vector to the left by 90 degree to get normal
	unit_normal = (start[1]-target[1],target[0]-start[0])

	return (mid[0]+DIST*unit_normal[0],mid[1]+DIST*unit_normal[1])

def draw_edges(w,V,E,scaling,edge_count,edge_count_def) :
	dir_color = {"N": "blue", "U": "blue", "S": "red", "D": "red", "W": "green", "E": "orange"}

	for edge in E :
		if edge.dir in dir_color.keys() :
			color = dir_color[edge.dir]
		else :
			color = "black"
		start = V[edge.start-1]
		target = V[edge.target-1]

		number_in = edge_count_def[(start.id,target.id)]
		number_out = edge_count_def[(target.id,start.id)]
		if number_in + number_out == 1 :
			w.create_line(int(scaling*start.x[0])
				,int(scaling*start.x[1])
				,int(scaling*target.x[0])
				,int(scaling*target.x[1])
				,width=0.1
				,smooth=1
				,arrow="last"
				,fill=color)
		else :
			DIST = 0.2*edge_count[(start.id,target.id)]
			edge_count[(start.id,target.id)] -= 1
			cnode = get_edge_curve_node(start.x,target.x,DIST)

			w.create_line(int(scaling*start.x[0])
				,int(scaling*start.x[1])
				,int(scaling*cnode[0])
				,int(scaling*cnode[1])
				,int(scaling*target.x[0])
				,int(scaling*target.x[1])
				,width=0.1
				,smooth=1
				,arrow="last"
				,fill=color)

		
def apply(master,w_width,w_height,arc_rad) :
	w = Canvas(master, width=w_width, height=w_height)
	w.pack()
	scaling = w_width
	width = 1
	height = 9/16

	# V must be sorted by id correctly
	# V = [Node(1)
	# 	,Node(2)
	# 	,Node(3)
	# 	,Node(4)]

	# E = [Edge(0,2,1,dir="E"), Edge(1,4,2,dir="N"), Edge(2,2,3,dir="S")]

	V = []
	E = []
	area_list = get_areas(V)

	# init edge_count
	edge_count = {}
	for start in V :
		for target in V :
			edge_count[(start.id,target.id)] = 0

	# edge_count = {(2,1): 1, (4,2): 1, (2,3): 1}
	edge_count_def = edge_count

	path_list = get_paths(V,E,edge_count)

	# init node coordinates
	random_coords(V,width,height)

	G = Graph(V,E,0.1)

	# force direction
	tolerance = True
	step = 0
	while tolerance :
		# sleep(1)

		if step == 500 :
		 	break
		
		# update node coordinates
		tolerance = G.update(width,height,step)

		# clear window
		w.delete("all")

		edge_count = deepcopy(edge_count_def)

		# draw final graph
		draw_nodes(w,V,arc_rad,w_width,w_height,scaling)
		draw_edges(w,V,E,scaling,edge_count,edge_count_def)
		
		w.update()
		step += 1

	w.postscript(file="map.ps", colormode='color')
	#mainloop()

	return G, area_list, path_list