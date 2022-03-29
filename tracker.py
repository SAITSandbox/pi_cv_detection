import math

class EuclideanDistTracker:

	
	def __init__(self):
		# Store the center positions of the objects
		self.center_points = {}
		# Keep the count of the IDs
		# each time a new object id detected, the count will increase by one
		self.id_count = 0


	def update(self, detection):
		# Objects boxes and ids
		objects_bbs_ids = []
		x, y, w, h = detection.bounding_box
		index = detection.categories[0][0]
		# Get center point of new object
		cx = (x + x + w) // 2
		cy = (y + y + h) // 2
		change_threshold = w/2

		# Find out if that object was detected already
		same_object_detected = False
		for id, pt in self.center_points.items():
			dist = math.hypot(cx - pt[0], cy - pt[1])

			if dist < change_threshold:
				self.center_points[id] = (cx, cy)
				# print(self.center_points)
				objects_bbs_ids.append([x, y, w, h, id, index])
				same_object_detected = True
				break

		# New object is detected we assign the ID to that object
		if same_object_detected is False:
			self.center_points[self.id_count] = (cx, cy)
			objects_bbs_ids.append([x, y, w, h, self.id_count, index])
			self.id_count += 1

		# Clean the dictionary by center points to remove IDS not used anymore
		new_center_points = {}
		for obj_bb_id in objects_bbs_ids:
			_, _, _, _, object_id, index = obj_bb_id
			center = self.center_points[object_id]
			new_center_points[object_id] = center

		# Update dictionary with IDs not used removed
		self.center_points = new_center_points.copy()
		print(objects_bbs_ids)
		return objects_bbs_ids