# To draw or fill a box or ellipse around a label or frame and return the boundary as a path, use one of the predefined envelope routines

# path box(frame f, Label L="", real xmargin=0,
#          real ymargin=xmargin, pen p=currentpen,
#          filltype filltype=NoFill, bool above=true);

class AsyFile :
	def __init__(self,file,Graph,area_list,path_list) :
		self.filename = file
		self.G = Graph
		self.area_list = area_list
		self.path_list = path_list
		self.file = None

	def write_header(self) :
		header = """size(0,200);
					real margin=1mm; \n"""
		self.file.write(header)

	def define_vars(self) :
		light_vars = """pen no_light = rgb("9ca0a8");
						pen light = rgb("f4f142"); \n"""
		self.file.write(light_vars)

	def write_boxes(self) :
		for node in self.G.V :
			light = "light"
			if type(node.id) == str :
				pass	# NON%d
			else :
				area = self.area_list[node.id-1]
				if area["light"] == True :
					light = "light"
				else :
					light = "no_light"
			self.file.write("""object Room%d = draw("%s", box, (%f,%f), margin, %s); \n"""
						%(node.id, area["name"], node.x[0], node.x[1], light))
		return 0

	def write_arrows(self) :
		return 0

	def write_file(self) :
		self.file = open(self.filename,"w")
		self.write_header()
		self.define_vars()
		self.write_boxes()
		self.file.close()
