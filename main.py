from tkinter import *
from random import random
from graph import Node, Edge, Graph
from time import sleep
import records

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
		node.x = (t_w*width,t_h*height)

# place nodes according to the coordinates as ovals in canvas
def draw_nodes(w,V,arc_rad,width,height) :
	for node in V :
		w.create_oval(int(node.x[0]+arc_rad)
			,int(node.x[1]+arc_rad)
			,int(node.x[0]-arc_rad)
			,int(node.x[1]-arc_rad)
			,fill="blue")

def draw_edges(w,V,E,width,height) :
	for edge in E :
		start = V[edge.start-1]
		target = V[edge.target-1]
		w.create_line(int(start.x[0])
			,int(start.x[1])
			,int(target.x[0])
			,int(target.x[1])
			,width=2.5
			,smooth=1
			,arrow="last")



if __name__ == "__main__" :
	master = Tk()

	w_width = 1200
	w_height = 720
	arc_rad = 5

	w = Canvas(master, width=w_width, height=w_height)
	w.pack()


	# V must be sorted by id correctly
	# V = [Node(0)
	# 	,Node(1)
	# 	,Node(2)
	# 	,Node(3)
	# 	,Node(4)
	# 	,Node(5)
	# 	,Node(6)]

	# E = [Edge(0,0,1), Edge(1,0,2), Edge(2,1,2), Edge(3,0,3,dir="N"),Edge(4,4,0,dir="N"),Edge(5,1,5,dir="D"),Edge(6,5,6,dir="S")]
	# 	#, Edge(3,1,2), Edge(4,2,0), Edge(4,2,1)]

	V = []
	E = []
	get_areas(V)
	get_paths(E)

	print(len(V))
	print(len(E))

	# init node coordinates
	random_coords(V,w_width,w_height)

	G = Graph(V,E)

	# force direction
	while True :
		#sleep(0.01)
		
		# update node coordinates
		G.update(w_width,w_height)

		# clear window
		w.delete("all")
		# draw final graph
		draw_nodes(w,V,arc_rad,w_width,w_height)
		draw_edges(w,V,E,w_width,w_height)
		w.update()

	mainloop()