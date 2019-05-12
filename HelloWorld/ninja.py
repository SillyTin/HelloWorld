from binaryninja import *
import os
from graphviz import Digraph
from hello import models

funcs = {}
cg = {}
cfg = {}
cg_path = []
cfg_path = {}

class CfgPath:
	pass

def load_binary(path):

    # Load binary file
    bv = BinaryViewType['ELF'].get_view_of_file(path)
    print("Analysis %s done" % (path))

    return bv


def get_func(bv):

	# Get functions
	for func in bv.functions:
		addr = hex(int(func.start))
		funcs[addr] = func.symbol.name

	#store in db
	models.FuncInfo.objects.all().delete()	
	for i in funcs.keys():
		models.FuncInfo.objects.create(addr = i, name = funcs[i])

	print("get func")

def get_inst(bv):
    
	# Get instructions
	inst = []
	for i in bv.instructions:
		ins = ''
		for j in i[0]:
			ins = ins + str(j)
		inst.append("%s : %s" % (hex(int(i[1])), ins))

	# f = open("%sinst.txt" % (path) , "w")
	# for i in inst:
	# 	f.write("%s\n" % (i))
	# f.close()

	print("get inst")


def get_CG(bv):

	# Create CG
	for func in bv.functions:
		caller = hex(int(func.start))
		cg[caller] = []
		for inst in func.instructions:
			if func.is_call_instruction(inst[1]):
				if str(inst[0][-1]).startswith("0x"):
					if str(inst[0][-1]) not in cg[caller]:
						cg[caller].append(str(inst[0][-1]))
			if str(inst[0][0] == 'b'):
				des = str(inst[0][-1])
				if des in funcs.keys() and des not in cg[caller]:
					cg[caller].append(des)

	models.CallGraphEdge.objects.all().delete()
	models.CallGraphNode.objects.all().delete()
	i = 0
	cgnode = {}
	cgedge = []
	for caller in cg.keys():
		if cg[caller] != []:
			if caller not in cgnode.keys():
				cgnode[caller] = i
				i += 1
			for callee in cg[caller]:
				if callee not in cgnode.keys():
					cgnode[callee] = i
					i += 1
				cgedge.append((cgnode[caller],cgnode[callee]))
	for node in cgnode.keys():
		models.CallGraphNode.objects.create(num = cgnode[node] , name = funcs[node])
	for (i, j) in cgedge:
		models.CallGraphEdge.objects.create(start = i, end = j)

	print("get cg")


def get_cfg(bv):
    
	# Create CFG
	for func in bv.functions:
		func_name = hex(int(func.start))
		cfg[func_name] = {}
		for bb in func.basic_blocks:
			caller = hex(int(bb.start))
			cfg[func_name][caller] = []
			for edge in bb.outgoing_edges:
				callee = hex(int(edge.target.start))
				if callee not in cfg[func_name][caller]:
					cfg[func_name][caller].append(callee)

	# f = open("%scfg.txt" % (path) , "w")
	# for func in cfg.keys():
	# 	flag = False
	# 	for item in cfg[func]:
	# 		if cfg[func][item] != []:
	# 			flag = True
	# 	if flag:
	# 		f.write("%s:\n" % (func))
	# 		for caller in cfg[func]:
	# 			if cfg[func][caller] != []:
	# 				for callee in cfg[func][caller]:
	# 					f.write("%s -> %s\n" % (caller , callee))
	# f.close()

	print("get cfg")

def get_func_path(cg):
    
	# Find path in func level
	start = '0x100a0'
	end = '0xd69c'
	findpath_cg(start, end, cg, cg_path)

	# f = open("%scg_path.txt" % (path) , "w")
	# for i in cg_path:
	# 	for j in i[:-1]:
	# 		f.write("%s -> " % (j))
	# 	f.write("%s\n" % (i[-1]))
	# f.close()

	print("get cg_path")


def get_bb_path(cg_path, cfg):
    
	# Find path intro func in bb level

	# path = path +'cfg_path/'
	# isExists=os.path.exists(path)
	# if not isExists:
	# 	os.makedirs(path) 
	# 	print(path+' Create dir success')
	# else:
	# 	print(path+' already exists')

	for i in cg_path:
		for j in range(len(i)-1):
			start = i[j]
			end = i[j+1]
			name = "%s->%s" % (start, end)
			if name not in cfg_path.keys():
				cfg_path[name] = {}
				findpath_cfg(start, end, cfg[start], cfg_path[name])
				# f = open("%s%s-%s.txt" % (path, start, end) , "w")
				# for a in cfg_path[name].keys():
				# 	f.write("%s\n" % (a))
				# 	for b in cfg_path[name][a]:
				# 		f.write("-------------------------\n")
				# 		for c in b[:-1]:
				# 			f.write("%s -> " % (c))
				# 		f.write("%s\n" % (b[-1]))
				# 	f.write("----------------------------------------------------\n")

	print("get cfg_path")


def draw(list):
	g = Digraph('graph')
	for i in list:
		g.node(i,shape = 'box')
	for i in range(len(list)-1):
		g.edge(list[i],list[i+1])
	g.view()


def findpath_cg(start, end, cg, cg_path):

	related_node = [end]
	find_related_node(end, related_node, cg)
	path = []
	dfs(start, end, path, cg_path, cg, related_node)


def findpath_cfg(start, end, cfg_sin, cfg_path_sin):
	# cfg_sin: intro procedure, is a dirc
	# cfg_path_sin:{node->node:[[path1],[path2]]}, intro procedure

	dst_bb = find_dst_bb(start, end)

	for bb in dst_bb:
		dominators = []
		get_dominators(bb, dominators)
		for i in range(len(dominators)-1):
			start = hex(int(dominators[i+1].start))
			end = hex(int(dominators[i].start))
			name = "%s->%s" % (start,end)
			cfg_path_sin[name] = []
			findpath_cg(start, end, cfg_sin, cfg_path_sin[name])
			i += 1


def find_related_node(end, related_node, graph):
	
	for i in graph.keys():
		if end in graph[i]:
			if i not in related_node:
				related_node.append(i)
				find_related_node(i, related_node, graph)


def get_dominators(bb, dominators):
	# bb is binaryninja basic_block object
	# dominators is a list including dominators of bb

	global bv

	if bb.immediate_dominator:
		bb = bb.immediate_dominator
		dominators.append(bb)
		get_dominators(bb, dominators)

	print('get dominators')



def dfs(start, end, path, all_path, graph, related_node):
	# depth-first-search
	# start and end are strings of hex address in a graph
	# path is a list of node in a tmp path
	# all_path is a list including all paths from start to end
	# related_node is a list including all nodes related to end

	if len(all_path) > 1000:
		return

	if start == end:
		path.append(end)
		all_path.append(path.copy())
		path.pop()
	else:
		path.append(start)
		for i in graph[start]:
			if i not in path and i in related_node:
				dfs(i, end, path, all_path, graph, related_node)

		path.pop()


def find_dst_bb(src, dst):
	# src and dst are strings of hex address such as find_dst_bb('0x100a0', '0x19b3c')
	# dst_bb is a list including the bb will call the dst func

	src_addr = int(src,16)
	function = bv.get_function_at(src_addr)

	dst_bb = []
	for inst in function.instructions:
		if str(inst[0][-1]) == dst:
			dst_addr = int(str(inst[1]))
			dst_bb.append(function.get_basic_block_at(dst_addr))

	print("find dst bb")

	return dst_bb