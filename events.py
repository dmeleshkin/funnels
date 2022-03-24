from collections import namedtuple

EventDetails = namedtuple("EventDetails", "device, date, name, step, version, source, user, external, node, native")

def node(mAPINode, mAPI):
	if not mAPINode or mAPINode == "194.186.207.23":
		return int(mAPI) if mAPI else None
	elif mAPINode.startswith("greenfield1"):
		return 4
	elif mAPINode.startswith("node0"):
		return 0
	elif mAPINode.startswith("node1"):
		return 1
	elif mAPINode.startswith("node2"):
		return 2
	elif mAPINode.startswith("node3"):
		return 3
	elif mAPINode.startswith("node4"):
		return 5
	elif mAPINode.startswith("node5"):
		return 7
	elif mAPINode.startswith("node6"):
		return 8
	elif mAPINode.startswith("node7"):
		return 9

	return None
