'''
Look downwards to see the different levels.
Move forward to fall from one level to another. 
Press the spacebar to reset the viewpoint to
the top level.
'''

import viz
import vizact
import vizconnect
import vizmat
import vizshape
import vizinfo

vizinfo.InfoPanel()

resource = 'chao_grama.osgb'

vizconnect.go('config_faller.py')
vizconnect.getAvatar().getNode3d().disable(viz.INTERSECTION)

viz.clearcolor(viz.SLATE)
viz.addChild('scenario/'+resource,pos=[0,-20,0])
box = vizshape.addBox(size=(1,0.5,1),pos=[0,0,0],color=viz.BLUE)
box = vizshape.addBox(size=(4,0.5,4),pos=[0,-4,0],color=viz.GREEN)
box = vizshape.addBox(size=(9,0.5,9),pos=[0,-7,0],color=viz.GRAY)
box = vizshape.addBox(size=(13,0.5,13),pos=[0,-10,0],color=viz.PURPLE)
box = vizshape.addBox(size=(17,0.5,17),pos=[0,-15,0],color=viz.SKYBLUE)

vp = vizconnect.addViewpoint(pos=[0,0,0])
display = vizconnect.getDisplay()
vp.add(display)
vizact.onkeydown(' ',vizconnect.resetViewpoints)

class TrackedFaller(viz.VizNode):
	"""Class for simulating a head tracked user falling"""
	
	# Threshold to clamp height to ground level
	GROUND_CLAMP_THRESHOLD = 0.1
	
	# Distance from edge to allow before falling
	FALL_EDGE_BUFFER = 0.4
	
	# Maximum step height allowed
	STEP_HEIGHT = 0.3
	
	# Maximum fall velocity
	TERMINAL_VELOCITY = 60.0
	
	# Gravity acceleration
	GRAVITY = 9.8
	
	def __init__(self, tracker, transport, base=None):
		# Initialize using group node
		if base is None:
			group = viz.addGroup()
			viz.VizNode.__init__(self, group.id)
		else:
			viz.VizNode.__init__(self, base.id)
		
		self._tracker = tracker
		self._transport = transport
		
		self._disableTransportVerticalMovement = False
		self._offset = viz.Vector()
		self._velocity = 0.0
		
		# Update tracker every frame
		self._updater = vizact.onupdate(10, self.update)
	
	def _onFinishedFalling(self):
		"""Callback for when falling is complete"""
		pass
	
	def _intersect(self, begin, end):
		"""Call to trigger the intersect function"""
		return viz.intersect(begin, end, ignoreBackFace=True)
	
	def _clearVelocity(self):
		"""Clears the velocity of the faller"""	
		if self._velocity > 0.0:
			self._onFinishedFalling()
			self._velocity = 0.0
	
	def reset(self):
		"""Reset faller to origin"""
		self.setOffset([0, 0, 0])
		self._velocity = 0.0
	
	def setOffset(self, offset):
		"""Set offset"""
		oldOffset = vizmat.Vector(self._offset)
		self._offset.set(offset)
		self.setPosition(vizmat.Vector(self.getPosition(viz.ABS_GLOBAL))+self._offset-oldOffset, viz.ABS_GLOBAL)
	
	def getVelocity(self):
		"""Returns the veloicty of the faller"""
		return self._velocity
	
	def update(self, instantFall=False):
		"""Updates the position, velocity, etc of the faller"""
		# Get tracker position
		if self._disableTransportVerticalMovement:
			transport_pos = self._transport.getPosition()
			transport_pos[1] = 0
			self._transport.setPosition(transport_pos)
		
		tracker_pos = self._tracker.getPosition(viz.ABS_GLOBAL)
		tracker_pos[1] = self._transport.getPosition(viz.ABS_GLOBAL)[1]
		selfPos = self.getPosition(viz.ABS_GLOBAL)
		
		# Get current view position
		view_pos = vizmat.Vector(tracker_pos)
		view_pos[1] += self.STEP_HEIGHT
		
		# Perform intersection to determine height of view above ground
		line_end = view_pos - [0, 500, 0]
		isections = [self._intersect(view_pos, line_end)]
		
		# Check points around position to allow buffer around edges
		if self.FALL_EDGE_BUFFER > 0.0:
			buf = self.FALL_EDGE_BUFFER
			isections.append(self._intersect(view_pos+[buf, 0, 0], line_end+[buf, 0, 0]))
			isections.append(self._intersect(view_pos+[-buf, 0, 0], line_end+[-buf, 0, 0]))
			isections.append(self._intersect(view_pos+[0, 0, buf], line_end+[0, 0, buf]))
			isections.append(self._intersect(view_pos+[0, 0, -buf], line_end+[0, 0, -buf]))
		
		# Get intersection with largest height
		try:
			info = max((info for info in isections if info.valid), key=lambda info: info.point[1])
		except ValueError:
			info = isections[0]
		
		# if the center intersection is only slightly lower (step height), favor that
		if isections[0].point[1]+self.STEP_HEIGHT > info.point[1]:
			info = isections[0]
		
		if info.valid:
			if instantFall:
				self._offset[1] = info.point[1]
				self._clearVelocity()
			else:
				# Get height above ground
				ground_height = info.point[1]
			
				# If current offset is greater than ground height, then apply gravity
				if self._offset[1] > ground_height:
					dt = viz.getFrameElapsed()
					self._velocity = min(self._velocity + (self.GRAVITY * dt), self.TERMINAL_VELOCITY)
					self._offset[1] -= (self._velocity * dt)
			
				# Clamp to ground level if fallen below threshold
				if self._offset[1] - self.GROUND_CLAMP_THRESHOLD < ground_height:
					self._offset[1] = ground_height
					self._clearVelocity()
		
		# Update position/orientation
		self.setPosition(selfPos[0], self._offset[1], selfPos[2], viz.ABS_GLOBAL)


class CustomTrackedFaller(TrackedFaller):
	"""Derived tracked faller class for performing action when finished falling"""
	def _onFinishedFalling(self):
		if self.getVelocity() > 6.0:
			print("finished falling")


# Create tracked faller and link to main view
faller = CustomTrackedFaller(tracker=vizconnect.getAvatar().getNode3d(),
							transport=vizconnect.getTransport().getNode3d(),
							base=vizconnect.getMovableNode().getNode3d())