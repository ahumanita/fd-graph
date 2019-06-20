from math import sqrt

class Node :
	def __init__(self,id,x=(0,0),v=(0,0),a=(0,0),m=1) :
		self.x = x
		self.v = v
		self.a = a
		self.m = m
		self.id = id

class Edge :
	def __init__(self,id,start,target,dir="") :
		self.id = id
		self.start = start
		self.target = target
		self.dir = dir

class Graph :
	def __init__(self,V,E) :
		self.V = V
		self.E = E

	def electric_force_update(self,force,node) :
		for mnode in self.V :
			if mnode != node :
				dist = sqrt((node.x[0]-mnode.x[0])**2 + (node.x[1]-mnode.x[1])**2)
				node.a = (node.a[0]+(node.x[0]-mnode.x[0])*force/(dist**3)
							,node.a[1]+(node.x[1]-mnode.x[1])*force/(dist**3))

	# (gx,gy) is the point node is gravitated by
	@staticmethod
	def gravity_to_update(gravity,node,attractor) :
		# mass = 9000
		# dist = sqrt((node.x[0]-attractor[0])**2 + (node.x[1]-attractor[1])**2)
		# node.a = (node.a[0]-gravity*mass*(node.x[0]-attractor[0])/dist**2
		# 			,node.a[1]-gravity*mass*(node.x[1]-attractor[1])/dist**2)
		dist = sqrt((node.x[0]-attractor[0])**2 + (node.x[1]-attractor[1])**2)
		node.a = (node.a[0]-(node.x[0]-attractor[0])*gravity/(dist**3)
					,node.a[1]-(node.x[1]-attractor[1])*gravity/(dist**3))

	def feather_update(feather,start,target) :
		start.a = (start.a[0]-edge.feather*(start.x[0]-target.x[0])
					,start.a[1]-edge.feather*(start.x[1]-target.x[1]))
		target.a = (target.a[0]-edge.feather*(target.x[0]-start.x[0])
					,target.a[1]-edge.feather*(target.x[1]-start.x[1]))

	def edge_orientation_update(gravity,start,node,dir) :
		dist = sqrt((node.x[0]-start.x[0])**2 + (node.x[1]-start.x[1])**2)
		tol = 2*dist/3
		dir_coeff = {"N": (0,-1), "U": (0,-1)
					, "S": (0,1), "D": (0,1)
					, "E": (-1,0), "W": (1,0)
					, "NE": (-1,-1), "NW": (1,-1)
					, "SE": (-1,1), "SW": (1,1)
					, "OUT": (0,0)}
		# if edge.dir == "N" or edge.dir == "U" :
		if edge.dir in dir_coeff.keys() :
			# # avoid that start node sticks to top
			# if start.x[1] < tol :
			# 	start.a = (start.a[0],start.a[1]-gravity*(start.a[1]-height)/dist**3)

			# # avoid that start node sticks to right
			# if abs(start.x[0]-width) < tol :
			# 	start.a = (start.a[0]-gravity*(start.a[0]-width)/dist**3,start.a[1])

			# # avoid that start node sticks to left
			# if start.x[0] < tol :
			# 	start.a = (start.a[0]-gravity*(start.a[0]-width)/dist**3,start.a[1])

			# gravity to north
			if node.x[1] > tol and node.x[0] != start.x[0] :
				imx = start.x[0] + dir_coeff[edge.dir][0]*dist
				imy = start.x[1] + dir_coeff[edge.dir][1]*dist
				gravity_to_update(gravity,node,(imx,imy))

	def update(self,width,height) :
		feather = 0.005
		elec = 500
		gravity_center = 1
		drag = 0.9
		gravity_orient = 500

		center = (int(width/2),int(height/2))

		# reset acceleration
		for node in self.V :
			node.a = (0,0)

		for edge in self.E :
			start = self.V[edge.start-1]
			target = self.V[edge.target-1]
			#feather_update(feather,start,target)
			#edge_orientation_update(gravity_orient,start,target,edge.dir)

		for node in self.V :
			self.electric_force_update(elec,node)	

			# drag update
			node.a = (node.a[0]-node.v[0]*drag,node.a[1]-node.v[1]*drag)

			# velocity update
			node.v = (node.a[0]+node.v[0],node.a[1]+node.v[1])

			# coord update
			upd = (node.x[0]+node.v[0], node.x[1]+node.v[1])

			# get away from boundary
			if upd[0] >= width :
				node.v = (min(-node.v[0],node.v[0]),node.v[1])
			elif upd[0] <= 0 :
				node.v = (max(-node.v[0],node.v[0]),node.v[1])
			if upd[1] >= height :
				node.v = (node.v[0],min(-node.v[1],node.v[1]))
			elif upd[1] <= 0 :
				node.v = (node.v[0],max(-node.v[1],node.v[1]))

			# gravity update
			dist_cent = sqrt((node.x[0]-center[0])**2 + (node.x[1]-center[1])**2)
			upd = (node.x[0]+node.v[0]-(node.x[0]-center[0])/dist_cent, node.x[1]+node.v[1]-(node.x[1]-center[1])/dist_cent)

			node.x = (upd[0], upd[1])