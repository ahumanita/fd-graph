from math import sqrt

class Node :
	def __init__(self,id,x=(0,0),v=(0,0),a=(0,0),m=1) :
		self.x = x
		self.v = v
		self.a = a
		self.m = m
		self.id = id

class Edge :
	def __init__(self,id,start,target,feather=0.001,dir="") :
		self.id = id
		self.start = start
		self.target = target
		self.feather = feather
		self.dir = dir

class Graph :
	def __init__(self,V,E) :
		self.V = V
		self.E = E

	def update(self,width,height) :
		# reset acceleration
		for node in self.V :
			node.a = (0,0)

		for edge in self.E :
			# feather update
			start = self.V[edge.start]
			target = self.V[edge.target]
			start.a = (start.a[0]-edge.feather*(start.x[0]-target.x[0])
						,start.a[1]-edge.feather*(start.x[1]-target.x[1]))
			target.a = (target.a[0]-edge.feather*(target.x[0]-start.x[0])
						,target.a[1]-edge.feather*(target.x[1]-start.x[1]))

			# directions
			gravity = 5000
			node = self.V[edge.target]
			start = self.V[edge.start]
			dist = sqrt((node.x[0]-start.x[0])**2 + (node.x[1]-start.x[1])**2)
			tol = 2*dist/3

			if edge.dir == "N" or edge.dir == "U" :
				# avoid that start node sticks to top
				if start.x[1] < tol :
					start.a = (start.a[0],start.a[1]-gravity*(start.a[1]-height)/dist**3)

				# avoid that start node sticks to right
				if abs(start.x[0]-width) < tol :
					start.a = (start.a[0]-gravity*(start.a[0]-width)/dist**3,start.a[1])

				# gravity to north
				if node.x[1] > tol and node.x[0] != start.x[0] :
					imx = start.x[0]
					imy = start.x[1]-dist
					distim = sqrt((node.x[0]-imx)**2 + (node.x[1]-imx)**2)
					node.a = (node.a[0]-gravity*(node.x[0]-imx)/distim**3
								,node.a[1]-gravity*(node.x[1]-imy)/distim**3)

			if edge.dir == "S" or edge.dir == "D" :
				# avoid that start node sticks to bottom
				if abs(start.x[1]-height) < tol :
					start.a = (start.a[0],start.a[1]-gravity*(start.a[1]-height)/dist**3)

				# avoid that start node sticks to right
				if abs(start.x[0]-height) < tol :
					start.a = (start.a[0]-gravity*(start.a[0]-height)/dist**3,start.a[1])

				# gravity to north
				if node.x[1] < height and node.x[0] != start.x[0] :
					imx = start.x[0]
					imy = start.x[1]+dist
					dist = sqrt((node.x[0]-imx)**2 + (node.x[1]-imx)**2)
					node.a = (node.a[0]-gravity*(node.x[0]-imx)/dist**3
								,node.a[1]-gravity*(node.x[1]-imy)/dist**3)

		for node in self.V :
			# electric force update
			elec = 500
			for mnode in self.V :
				if mnode != node :
					dist = sqrt((node.x[0]-mnode.x[0])**2 + (node.x[1]-mnode.x[1])**2)
					node.a = (node.a[0]+(node.x[0]-mnode.x[0])*elec/(dist**3)
								,node.a[1]+(node.x[1]-mnode.x[1])*elec/(dist**3))

			# drag update
			drag = 0.1
			node.a = (node.a[0]-node.v[0]*drag,node.a[1]-node.v[1]*drag)

			# velocity update
			node.v = (node.a[0]+node.v[0],node.a[1]+node.v[1])

			# coord update
			upd = (node.x[0]+node.v[0], node.x[1]+node.v[1])

			# TODO: min ( -node.v[0],node.v[0])
			if upd[0] >= width :
				node.v = (min(-node.v[0],node.v[0]),node.v[1])
			elif upd[0] <= 0 :
				node.v = (max(-node.v[0],node.v[0]),node.v[1])
			if upd[1] >= height :
				node.v = (node.v[0],min(-node.v[1],node.v[1]))
			elif upd[1] <= 0 :
				node.v = (node.v[0],max(-node.v[1],node.v[1]))

			upd = (node.x[0]+node.v[0], node.x[1]+node.v[1])

			node.x = (upd[0], upd[1])