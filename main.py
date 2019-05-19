from tkinter import *
from random import random
from graph import Node, Edge, Graph
from time import sleep

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
		start = V[edge.start]
		target = V[edge.target]
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

	V = [Node(0,Adj=[1,2])
		,Node(1,Adj=[0,2])
		,Node(2,Adj=[0,1])]

	E = [Edge(0,0,1), Edge(1,0,2), Edge(2,1,2)]
		#, Edge(3,1,2), Edge(4,2,0), Edge(4,2,1)]

	# init node coordinates
	random_coords(V,w_width,w_height)

	G = Graph(V,E)

	# force direction
	while True :
		sleep(0.05)
		
		# update node coordinates
		G.update(w_width,w_height)

		# clear window
		w.delete("all")
		# draw final graph
		draw_nodes(w,V,arc_rad,w_width,w_height)
		draw_edges(w,V,E,w_width,w_height)
		w.update()

	mainloop()