import math

def getDistance(civ1, civ2):
		return round(math.sqrt(((civ1.X-civ2.X)**2)+((civ1.Y-civ2.Y)**2)),2)

def getQuad(origin, target):
	if target.X >= origin.X and target.Y >= origin.Y:	# 目标文明在发送者为中心的第一象限（右上角）
		return 1

	elif target.X >= origin.X and target.Y <= origin.Y:	# 目标文明在发送者为中心的第四象限（右下角）
		return 4

	elif target.X <= origin.X and target.Y >= origin.Y:	# 目标文明在发送者为中心的第二象限（左上角）
		return 2

	elif target.X <= origin.X and target.Y <= origin.Y:	# 目标文明在发送者为中心的第三象限（左下角）
		return 3

def calculateAngle(origin, target, convey):
	'''
	return the degree angle of origin to target 
	'''
	if target.X >= origin.X and target.Y >= origin.Y:	# 目标文明在发送者为中心的第一象限（右上角）
		return math.asin(abs(target.X-origin.X)/convey.Distance)*(180/math.pi)

	elif target.X >= origin.X and target.Y <= origin.Y:	# 目标文明在发送者为中心的第四象限（右下角）
		return math.asin(-1*abs(target.X-origin.X)/convey.Distance)*(180/math.pi)

	elif target.X <= origin.X and target.Y >= origin.Y:	# 目标文明在发送者为中心的第二象限（左上角）
		return math.acos(-1*abs(target.X-origin.X)/convey.Distance)*(180/math.pi)

	elif target.X <= origin.X and target.Y <= origin.Y:	# 目标文明在发送者为中心的第三象限（左下角）
		temp = math.acos(-1*abs(target.X-origin.X)/convey.Distance)
		return ((math.pi - temp) + math.pi)*(180/math.pi)