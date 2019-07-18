from tkinter import *
from random import random
from graph import Node, Edge, Graph
from time import sleep
import records
from math import sqrt

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
       	# TODO: kann man bestimmt in Schleife packen!

        act_area["name"] = place[0]["name"]
        act_area["id"] = place[0]["id"]       
        area_list.append(act_area)
        
        V.append(Node(i))
        i += 1
    return area_list

#p_id: path id, st: start, des: destination, num_d: number of directions, d#: direction, col: color
#TODO keys anzeigen (ort)
def get_paths(E) :
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

		#check if destination is null or not
		if not path :
			pass
			# path = db.query("""SELECT  path.id, path.start, path.destination, path.direction,
			# 	path.usable, path.information, path.waterpath, path.notes FROM path WHERE path.id = :p_id"""
			# 	, p_id = i)
			# act_path["destination"] = "NON%d" %(i)
			# graph.node("NON%d" %(i), "???")
		else :
			act_path["destination"] = path[0]["destination"]

			act_path["id"] = path[0]["id"]
			act_path["start"] = path[0]["start"]
			act_path["direction"] = path[0]["direction"]
			path_list.append(act_path)
			E.append(Edge(i,int(path[0]["start"]),int(path[0]["destination"]),dir=path[0]["direction"]))
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

def draw_edges(w,V,E,w_width,w_height,scaling) :
	dir_color = {"N": "blue", "U": "blue", "S": "red", "D": "red", "W": "green", "E": "orange"}

	for edge in E :
		if edge.dir in dir_color.keys() :
			color = dir_color[edge.dir]
		else :
			color = "black"
		start = V[edge.start-1]
		target = V[edge.target-1]

		DIST = 0.1
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



if __name__ == "__main__" :
	master = Tk()

	w_width = 1200
	w_height = 720

	width = 1
	height = 9/16

	arc_rad = 1
	scaling = w_width

	w = Canvas(master, width=w_width, height=w_height)
	w.pack()


	# V must be sorted by id correctly
	# V = [Node(0)
	# 	,Node(1)
	# 	,Node(2)
	# 	,Node(3)]

	# E = [Edge(0,0,1,dir="E"), Edge(1,0,2,dir="N"), Edge(2,2,3,dir="S")]

	V = []
	E = []
	get_areas(V)
	get_paths(E)
	# init node coordinates
	random_coords(V,width,height)

	G = Graph(V,E,0.1)

	# force direction
	tolerance = True
	step = 0
	while tolerance :
		# sleep(1)

		# if step == 4 :
		# 	break
		
		# update node coordinates
		tolerance = G.update(width,height,step)

		# clear window
		w.delete("all")

		# draw final graph
		draw_nodes(w,V,arc_rad,w_width,w_height,scaling)
		draw_edges(w,V,E,w_width,w_height,scaling)
		w.update()
		step += 1

	w.postscript(file="map.ps", colormode='color')
	#mainloop()