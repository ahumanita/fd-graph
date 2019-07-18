from math import sqrt, acos

class Node :
	def __init__(self,id,x=(0,0),v=(0,0),a=(0,0),m=1) :
		self.x = x
		self.v = v
		self.a = a
		self.m = m
		self.id = id
		self.orient = (0,0)

class Edge :
	def __init__(self,id,start,target,dir="") :
		self.id = id
		self.start = start
		self.target = target
		self.dir = dir

class Graph :
	def __init__(self,V,E,tolerance) :
		self.V = V
		self.E = E
		self.tolerance = tolerance
		# i somehow had a sign error, this fits, dunno why
		self.dir_coeff = {"N": (0,1), "U": (0,1)
					, "S": (0,-1), "D": (0,-1)
					, "E": (-1,0), "W": (1,0)
					, "NE": (-1,-1), "NW": (1,-1)
					, "SE": (-1,1), "SW": (1,1)
					, "OUT": (0,0)}

	def electric_force_update(self,force,node) :
		for mnode in self.V :
			if mnode != node :
				dist = sqrt((node.x[0]-mnode.x[0])**2 + (node.x[1]-mnode.x[1])**2)
				node.a = (node.a[0]+(node.x[0]-mnode.x[0])*force/(dist**3)
							,node.a[1]+(node.x[1]-mnode.x[1])*force/(dist**3))

	# (gx,gy) is the point node is gravitated by
	@staticmethod
	def gravity_to_update(gravity,node,attractor) :
		dist = sqrt((node.x[0]-attractor[0])**2 + (node.x[1]-attractor[1])**2)
		node.a = (node.a[0]-gravity*(node.x[0]-attractor[0])/dist**2
					,node.a[1]-gravity*(node.x[1]-attractor[1])/dist**2)

	def feather_update(self,feather,start,target) :
		start.a = (start.a[0]-feather*(start.x[0]-target.x[0])
					,start.a[1]-feather*(start.x[1]-target.x[1]))
		target.a = (target.a[0]-feather*(target.x[0]-start.x[0])
					,target.a[1]-feather*(target.x[1]-start.x[1]))

	def edge_orientation_update(self,const,start,node,dir) :
		dist = sqrt((node.x[0]-start.x[0])**2 + (node.x[1]-start.x[1])**2)
		tol = 2*dist/3
		# if edge.dir == "N" or edge.dir == "U" :
		if dir in self.dir_coeff.keys() :
			update = (0,0)
			# gravity to north
			if node.x[1] > tol and node.x[0] != start.x[0] :
				imx = start.x[0] + self.dir_coeff[dir][0]*dist
				imy = start.x[1] + self.dir_coeff[dir][1]*dist
				#Graph.gravity_to_update(gravity,node,(imx,imy))
				dist = sqrt((node.x[0]-imx)**2 + (node.x[1]-imy)**2)
				update = (const*(node.x[0]-imx)/dist,const*(node.x[1]-imy)/dist)

			# add orientation again in every step, but not in velocity!
			node.orient = (node.orient[0]-update[0],node.orient[1]-update[1])

	def nonoverlapping_edges_update(self,edge,start,target) :
		for edge2 in self.E :
			if edge2 is edge :
				break
			start2 = self.V[edge2.start-1]
			target2 = self.V[edge2.target-1]
			# do they intersect?
			# target.x[0]-start.x[0]	-target2.x[0]+start2.x[0]	*	s 	= -start.x[0] + start2.x[0]
			# target.x[1]-start.x[1]	-target2.x[1]+start2.x[1]	*	t 	= -start.x[1] + start2.x[1]
			det = (target.x[0]-start.x[0])*(start2.x[1]-target2.x[1]) - (target.x[1]-start.x[1])*(start2.x[0]-target2.x[0])
			if det != 0 and edge.dir in self.dir_coeff.keys() :
				coeff = (1/det*((start2.x[1]-target2.x[1])*(start2.x[0]-start.x[0])+(target2.x[0]-start2.x[0])*(start2.x[1]-start.x[1]))
						,1/det*((start.x[1]-target.x[1])*(start2.x[0]-start.x[0])+(target.x[0]-start.x[0])*(start2.x[1]-start.x[1])))
				if 0 < coeff[0] < 1 and 0 < coeff[1] < 1 :
					dist = sqrt((start.x[0]-coeff[0])**2 + (start.x[1]-coeff[1])**2)
					start.orient = (start.orient[0]+self.dir_coeff[edge.dir][0]*(start.x[0]-coeff[0])/dist,start.orient[1]+self.dir_coeff[edge.dir][1]*(start.x[1]-coeff[1])/dist)
					start.orient = (target.orient[0]+self.dir_coeff[edge.dir][0]*(start.x[0]-coeff[0])/dist,target.orient[1]+self.dir_coeff[edge.dir][1]*(start.x[1]-coeff[1])/dist)

				# # get nearest point on line
				# rhs = - ((start2.x[0]-start.x[0])*(target2.x[0]-start2.x[0]) + (start2.x[1]-start.x[1])*(target2.x[0]-start2.x[0]))
				# coeff = (target2.x[0]-start2.x[0])**2 + (target2.x[1]-start2.x[1])**2
				# if coeff == 0 :
				# 	continue

				# param = rhs/coeff
				# # perpendicular point
				# perp = (start2.x[0]+param*(target2.x[0]-start2.x[0]),start2.x[1]+param*(target2.x[1]-start2.x[1]))
				# # distance from start to perp
				# dist = sqrt((start.x[0]-perp[0])**2 + (start.x[1]-perp[1])**2)
				# # add force that adds dist to the coords of start and target
				# if dist == 0 :
				# 	continue
				# #start.orient = (start.orient[0]+(start.x[0]-perp[0])/dist,start.orient[1]+(start.x[1]-perp[1])/dist)
				# # target.orient = (target.orient[0]+(start.x[0]-perp[0])/dist,target.orient[1]+(start.x[1]-perp[1])/dist)
				# const = 0.00005
				# start.orient = (start.orient[0]+self.dir_coeff[edge.dir][0]*const*(start.x[0]-perp[0]),start.orient[1]+self.dir_coeff[edge.dir][1]*const*(start.x[1]-perp[1]))
				# #target.orient = (target.orient[0]+self.dir_coeff[edge.dir][0]*const*(start.x[0]-perp[0]),target.orient[1]+self.dir_coeff[edge.dir][1]*const*(start.x[1]-perp[1]))



	def update(self,width,height,step) :
		feather = 0.001
		elec = 0.00000001
		drag = 0.09
		gravity_orient = 0
		C = 0.0005
		tolerance = True

		center = (width/2.,height/2.)

		# reset acceleration and orientation
		for node in self.V :
			node.a = (0,0)
			node.orient = (0,0)

		for edge in self.E :
			start = self.V[edge.start-1]
			target = self.V[edge.target-1]
			self.feather_update(feather,start,target)
			self.edge_orientation_update(C,start,target,edge.dir)
			# self.nonoverlapping_edges_update(edge,start,target)

		for node in self.V :
			self.electric_force_update(elec,node)	

			# drag update
			node.a = (node.a[0]-node.v[0]*drag,node.a[1]-node.v[1]*drag)

			# velocity update
			node.v = (node.a[0]+node.v[0],node.a[1]+node.v[1])

			# coord update
			upd = (node.x[0] + node.v[0] -node.orient[0], node.x[1] + node.v[1] -node.orient[1])

			# get away from boundary
			if upd[0] >= width :
				node.v = (min(-node.v[0],node.v[0]),node.v[1])
				node.orient = (0,0)
			elif upd[0] <= 0 :
				node.v = (max(-node.v[0],node.v[0]),node.v[1])
				node.orient = (0,0)
			if upd[1] >= height :
				node.v = (node.v[0],min(-node.v[1],node.v[1]))
				node.orient = (0,0)
			elif upd[1] <= 0 :
				node.v = (node.v[0],max(-node.v[1],node.v[1]))
				node.orient = (0,0)

			# final update + gravity update
			dist_cent = sqrt((node.x[0]-center[0])**2 + (node.x[1]-center[1])**2)
			upd = (node.v[0]-C*(node.x[0]-center[0])/dist_cent-node.orient[0] ,node.v[1]-C*(node.x[1]-center[1])/dist_cent -node.orient[1])
			#print(node.x[0] + upd[0])
			#print((node.x[0]-center[0])*dist_cent)
			# upd = (node.v[0] -node.orient[0],node.v[1] -node.orient[1])

			# check if change is large
			#if sqrt(upd[0]**2 + upd[1]**2) > self.tolerance :
			#	tolerance = True

			node.x = (node.x[0]+upd[0], node.x[1]+upd[1])

		return tolerance