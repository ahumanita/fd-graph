# To draw or fill a box or ellipse around a label or frame and return the boundary as a path, use one of the predefined envelope routines

# path box(frame f, Label L="", real xmargin=0,
#          real ymargin=xmargin, pen p=currentpen,
#          filltype filltype=NoFill, bool above=true);

class AsyFile :
	def __init__(self,file,Graph,area_list,path_list) :
		self.file = file
		self.G = Graph
		self.area_list = area_list
		self.path_list = path_list

	def write_header(self) :
		return 0

	def write_boxes(self) :
		for node in self.G.V :
			if type(node.id) == str :
				pass	# NON%d
			else :
				area = area_list[node.id]
				if area.light == True :
					file.append("object Room%id = path box(f, '%s' box , , " %(node.id, node.name))
				else :
					pass
		return 0

	def write_arrows(self) :
		return 0
