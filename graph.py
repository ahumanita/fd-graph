from math import sqrt

class Node :
	def __init__(self,id,x=(0,0),Adj=[],v=(0,0),a=(0,0),m=1) :
		self.x = x
		self.v = v
		self.a = a
		self.m = m
		self.id = id
		self.Adj = Adj

class Edge :
	def __init__(self,id,start,target,feather=0.0001) :
		self.id = id
		self.start = start
		self.target = target
		self.feather = feather

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


		for node in self.V :
			# velocity update
			node.v = (node.a[0]+node.v[0],node.a[1]+node.v[1])

			# coord update
			upd = (node.x[0]+node.v[0], node.x[1]+node.v[1])
			if upd[0] >= width or upd[0] <= 0 :
				node.v = (-node.v[0],node.v[1])
			if upd[1] >= height or upd[1] <= 0 :
				node.v = (node.v[0],-node.v[1])

			node.x = (upd[0], upd[1])

			# electric force update
			# elec = 100
			# for mnode in self.V :
			# 	if mnode != node :
			# 		dist = sqrt((node.x[0]-mnode.x[0])**2 + (node.x[1]-mnode.x[1])**2)
			# 		node.a = (node.a[0]+(node.x[0]-mnode.x[0])*elec/(dist**3)
			# 					,node.a[1]+(node.x[1]-mnode.x[1])*elec/(dist**3))