from tkinter import *
from database_to_graph import apply
from visualization_asymptote import *

master = Tk()

w_width = 1200
w_height = 720

arc_rad = 1

[G,area_list,path_list] = apply(master,w_width,w_height,arc_rad)

asy = AsyFile("map.asy",1500,G,area_list,path_list)
asy.write_file()