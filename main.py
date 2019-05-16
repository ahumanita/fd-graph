from tkinter import *
from random import random

# assert random coordinates to nodes of graph between 0 and 1
def random_coords(V) :
	coords = []
	for item in V :
		t_w = random()
		t_h = random()
		coords.append([t_w,t_h])
	return coords

# place nodes according to the coordinates as ovals in canvas
def draw_nodes(w,coords,arc_rad,width,height) :
	for item in coords :
		w.create_oval(int(item[0]*width+arc_rad)
			,int(item[1]*height+arc_rad)
			,int(item[0]*width-arc_rad)
			,int(item[1]*height-arc_rad)
			,fill="blue")

def draw_edges(w,Adj,coords,width,height) :
	for i in range(len(Adj)) :
		for edge in Adj[i] :
			w.create_line(int(coords[i][0]*width)
				,coords[i][1]*width
				,coords[edge][0]*width
				,coords[edge][1]*width
				)



if __name__ == "__main__" :
	master = Tk()

	w_width = 500
	w_height = 500
	arc_rad = 5

	w = Canvas(master, width=w_width, height=w_height)
	w.pack()

	V = [0,1,2]
	Adj = [[1,2],[0,2],[1,2]]

	coords = random_coords(V)
	draw_nodes(w,coords,arc_rad,w_width,w_height)
	draw_edges(w,Adj,coords,w_width,w_height)

	mainloop()