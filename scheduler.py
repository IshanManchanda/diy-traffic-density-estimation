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

		# Validate size of n_lanes
		assert len(n_lanes) == n_roads

		# Assign number of roads and lanes
		self.n_roads = n_roads
		self.n_lanes = n_lanes

		# Assign the algorithm coefficients and threshold
		self.k_current = k_c
		self.k_accumulation = k_a
		self.k_wait = k_w
		self.threshold = thresh

		# Lane that is currently green. Defaults to -1 if none given.
		# Verify that it is a valid road index and then assign
		assert -1 <= current < n_roads
		self.current = current

		# Initialize some additional attributes
		self.wait_times = [0] * self.n_roads  # Waiting times for each road
		self.confirmation = False  # Whether we're in confirmation mode
		self.conf_timer = 0  # How many time steps we've confirmed
		self.conf_steps = 4  # Number of time steps we're confirming
		self.conf_road = -1  # Road index we're watching for confirmation

	def update(self, detections):
		"""
		Constructs the Traffic Scheduler object.

		:param detections: List containing the number of detected vehicles
		at each of the roads. Must have length equal to n_roads.
		:type detections: List[int]

		:return: Tuple with 3 values: transition, confirmation, road_idx.
		1. transition is a boolean indicating
		whether a signal transition is required at this time step.
		2. confirmation is a boolean indicating whether the algorithm is
		currently in confirmation mode or not.
		The caller should adjust the polling rate accordingly.
		3. road_idx is an int which indicates the index of the road
		to transition to (in case transition is True) or the currently active
		road (when transition is False).
		:rtype: Tuple[bool, bool, int]
		"""

		# Validate size of detections
		assert len(detections) == self.n_roads

		# Update all wait times
		for i in range(self.n_roads):
			# Increment wait time for all roads except the currently active one.
			# If we're in confirmation mode, then interval is half time step
			# and otherwise it is one time step.
			if i != self.current:
				self.wait_times[i] += 1 if not self.confirmation else 0.5

		# If we're currently in confirmation mode, just invoke the
		# confirmation algorithm and return result
		if self.confirmation:
			return self._handle_confirmation(detections)

		# Compute traffic scores for each road and find road with max score
		traffic_scores, max_idx = self._compute_all_scores(detections)

		# If no road is currently active, simply use the maximum score road
		if self.current == -1:
			# Change_rn, increase_polling, change_to
			return True, False, max_idx

		# Compute difference in traffic score between max and current road
		score_diff = traffic_scores[max_idx] - traffic_scores[self.current]
		# Check if this difference exceeds our set threshold
		if score_diff >= self.threshold:
			self.confirmation = True
			self.conf_timer = 1
			self.conf_road = max_idx
			return False, True, self.current

		# Everything fine, we don't want to change the signal
		# and nor do we want to increase polling rate at the moment.
		return False, False, self.current

	def _compute_all_scores(self, detections):
		# TODO: Add docstring
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

		return traffic_scores, max_idx

	def _compute_traffic_score(self, current, accumulation, wait, n_lane):
		# TODO: Add docstring
		# Initialize score with the 'current' term
		score = self.k_current * current * n_lane

		# Add the 'accumulation' term
		score += self.k_accumulation * accumulation

		# Add the 'wait' term
		score += self.k_wait * wait ** 2

		return score

	def _handle_confirmation(self, detections):
		# TODO: Add docstring
		# Compute traffic scores for the current and confirmation road
		conf_score = self._compute_traffic_score(
			current=0, accumulation=detections[self.conf_road],
			wait=self.wait_times[self.conf_road],
			n_lane=self.n_lanes[self.conf_road]
		)
		current_score = self._compute_traffic_score(
			current=1, accumulation=detections[self.current],
			wait=0, n_lane=self.n_lanes[self.current]
		)

		# Compute difference in traffic score
		score_diff = conf_score - current_score
		# If difference less than threshold, confirmation fails.
		# Exit confirmation mode and return
		if score_diff < self.threshold:
			self.confirmation = False
			self.conf_timer = 0
			self.conf_road = -1
			return False, False, self.current

		# Difference is greater than or equal to the threshold,
		# we increment the confirmation timer
		self.conf_timer += 1

		# If we've not yet confirmed for the set number of time steps,
		# continue with the confirmation mechanism
		if self.conf_timer < self.conf_steps:
			return False, True, self.current

		# We've waited for the set number of time steps, perform transition.
		# Reset all waiting times to 0
		for i in range(self.n_roads):
			self.wait_times[i] = 0

		# Update current road and return values for signal transition
		self.current = self.conf_road
		return True, False, self.conf_road


