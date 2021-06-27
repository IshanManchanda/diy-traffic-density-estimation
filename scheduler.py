class Scheduler:
	"""
	Class to represent to Traffic Scheduler that manages the traffic signal
	at a particular intersection.
	"""

	def __init__(self, n_roads, n_lanes, k_c, k_a, k_w, thresh=10, current=-1):
		"""
		Constructs the Traffic Scheduler object.

		:param n_roads: Number of independent roads at this intersection
		:type n_roads: int
		:param n_lanes: List containing the number of lanes in each of the
		roads. Must have length equal to n_roads.
		:type n_lanes: List[int]

		:param k_c: k_current coefficient for the Scheduling algorithm
		:type k_c: float
		:param k_a: k_accumulation coefficient for the Scheduling algorithm
		:type k_a: float
		:param k_w: k_wait coefficient for the Scheduling algorithm
		:type k_w: float

		:param thresh: Traffic Score threshold to trigger a signal change
		:type thresh: float
		:param current: [Optional] Index of the road that is currently green.
		Defaults to -1 if none provided, which will give no road a priority
		during the first iteration of the algorithm.
		:type current: int
		"""
		# Assign number of roads and lanes
		self.n_roads = n_roads
		self.n_lanes = n_lanes

		# Validate size of n_lanes
		assert len(self.n_lanes) == self.n_roads

		# Assign the algorithm coefficients and threshold
		self.k_current = k_c
		self.k_accumulation = k_a
		self.k_wait = k_w
		self.threshold = thresh

		# Lane that is currently green. Defaults to -1 if none given.
		self.current = current
		# Verify that current is a valid road index
		assert -1 <= self.current < n_roads

		# Initialize some additional attributes
		self.wait_times = [0] * self.n_roads  # Waiting times for each road
		self.confirmation = False  # Whether we're in confirmation mode
		self.conf_timer = 0  # How many time steps we've confirmed

	def update(self, detections):
		"""
		Constructs the Traffic Scheduler object.

		:param detections: List containign the number of detected vehicles
		at each of the roads. Must have length equal to n_roads.
		:type detections: List[int]
		"""
		# TODO: Add return tuple to docstring

		# Validate size of detections
		assert len(detections) == self.n_roads

		# TODO: Handle confirmation mechanism
		#  essentially just compute the scores of max and current roads
		#  and check if it still exceeds the threshold
		#  if no, exit confirmation mode and return to normal behavior
		#  if yes, increment the confirmation timer.
		#  if confirmation timer hits limit, initiate change
		if self.confirmation:
			pass

		# Compute traffic scores for each road and find road with max score
		traffic_scores = []
		max_idx = 0
		for i in range(self.n_roads):

			# Compute score and append to the list
			traffic_scores.append(self._compute_traffic_score(
				current=1 if self.current == i else 0,
				accumulation=detections[i], wait=self.wait_times[i],
				n_lane=self.n_lanes[i]
			))

			# Check if maximum
			if traffic_scores[i] > traffic_scores[max_idx]:
				max_idx = i

		# If no road is currently active, simply use the maximum score road
		if self.current == -1:
			# Change_rn, increase_polling, change_to
			return True, False, max_idx

		# Compute difference in traffic score between max and current road
		score_diff = traffic_scores[max_idx] - traffic_scores[self.current]
		# Check if this difference exceeds our set threshold
		if score_diff >= self.threshold:
			# TODO: Trigger confirmation mechanism
			self.confirmation = True
			self.conf_timer = 1
			return False, True, max_idx

		# Everything fine, we don't want to change the signal
		# and nor do we want to increase polling rate at the moment.
		return False, False, self.current

	def _compute_traffic_score(self, current, accumulation, wait, n_lane):
		# TODO: Add docstring
		# Initialize score with the 'current' term
		score = self.k_current * current * n_lane

		# Add the 'accumulation' term
		score += self.k_accumulation * accumulation

		# Add the 'wait' term
		score += self.k_wait * wait ** 2

		return score
