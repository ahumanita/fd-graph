class AsyFile :
	def __init__(self,file,size,Graph,area_list,path_list) :
		self.filename = file
		self.size = size
		self.G = Graph
		self.area_list = area_list
		self.path_list = path_list
		self.file = None

	def write_header(self) :
		header = """size(0,%d);
					real margin=1mm; \n""" %(self.size)
		self.file.write(header)

	def define_vars(self) :
		light_vars = """pen no_light = rgb("9ca0a8");
						pen light = rgb("f4f142"); \n"""
		path_col_vars = """pen defaultpath = rgb("000000");
							pen unusable = rgb("ff5959");
							pen waterpath = rgb("3589ff");
							pen unusable_waterpath = rgb("c246c4"); \n"""
		path_vars = "pair outgoing = (0,0); \npair incoming = (0,0);\n"

		self.file.write(light_vars)
		self.file.write(path_col_vars)
		self.file.write(path_vars)

	def write_boxes(self) :
		# TODO: icons are missing, NONs are missing
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
			# this returns the bounding box object as Romm%d
			self.file.write("""object Room%d = draw("%s", box, (%f,%f), margin, %s); \n"""
						%(node.id, area["name"], self.size*node.x[0], -self.size*node.x[1], light))

	def write_paths(self) :
		asy_dir = {"N": "N", "E": "E", "S": "S", "W": "W",
					"NE": "NE", "NW": "NW", "SE": "SE", "SW": "SW",
					"U": "NNW", "D": "SSE", "OUT": "NNW", "IN": "SSE",
					"L": "N", "DS": "S", "US": "N"}
		inv_asy_dir = {"S": "N", "W": "E", "N": "S", "E": "W",
					"SW": "NE", "SE": "NW", "NW": "SE", "NE": "SW",
					"D": "NNW", "U": "SSE", "IN": "NNW", "OUT": "SSE",
					"L": "S", "US": "S", "DS": "N"}
		#TODO: destination NON case
		for edge in self.G.E :
			color = "defaultpath"
			path = self.path_list[edge.id-1]
			if path["waterpath"] == False :
				if path["usable"] == False :
					color = "unusable"
				else :
					color = "defaultpath"
			else :
				if path["usable"] == False :
					color = "unusable_waterpath"
				else :
					color = "waterpath"

			# check if target is lower or upper
			start = self.G.V[edge.start-1]
			target = self.G.V[edge.target-1]

			outgoing = ""
			incoming = ""
			if -start.x[1] > -target.x[1] :
				outgoing = "S"
				incoming = "N"
			elif -start.x[1] <= -target.x[1] :
				outgoing = "N"
				incoming = "S"

			self.file.write("""add(new void(frame f, transform t) {
								   draw(f,point(Room%d,%s,t)..point(Room%d,%s,t),Arrow);
								}); \n"""
							%(path["start"],outgoing,path["destination"],incoming))
							# %(path["start"],asy_dir[path["direction"]],
							# 	path["destination"],inv_asy_dir[path["direction"]]))
			# self.file.write("""draw(point(Room%d,up,0)..point(Room%d,SW)); \n"""
			# 				%(path["start"],path["destination"]))
							# %(path["start"],path["direction"],inv_edge_dir,path["destination"]))
		return 0

	def write_file(self) :
		self.file = open(self.filename,"w")
		self.write_header()
		self.define_vars()
		self.write_boxes()
		self.write_paths()
		self.file.close()
