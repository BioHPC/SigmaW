#!/usr/bin/env python

import os, glob, sys
def sigma_visualization(toolPath, toolIn, kronaPath, pTreePath):
	command = toolPath + ' ' + toolIn + ' ' + pTreePath
	os.system(command)
	kronaIn = []
	kronaIn.append(toolIn+'_krona1')
	kronaIn.append(toolIn+'_krona2')
	for k in range(len(kronaIn)):
		command = kronaPath + ' -o ' + kronaIn[k] + '.html ' + kronaIn[k]
		os.system(command)

def init_argv():
	toolPath = "/data1/thkim/run/sigma/cancer/a.out"
	toolIn = ""
	kronaPath = "/data1/thkim/run/KronaTools-2.7/scripts/ImportText.pl"
	pTreePath = "/data1/thkim/coding/javaProject/blastTool/created_from_complete_savedNodes_151123.txt"
	
	for i in range(len(sys.argv)):
		if sys.argv[i] == "-kp" : kronaPath  = sys.argv[i+1]
		if sys.argv[i] == "-tp": toolPath = sys.argv[i+1]
		if sys.argv[i] == "-ti": toolIn = sys.argv[i+1]
		if sys.argv[i] == "-pp": pTreePath = sys.argv[i+1]
		if sys.argv[i] == "-nt": 
			pTreePath = "noTaxonomyInfo"
			if toolPath == "/data1/thkim/go/run/sigma/cancer/a.out": toolPath = "/data1/thkim/run/sigma/cancer/b.out"
	return toolPath, toolIn, kronaPath, pTreePath

if __name__ == "__main__":
	toolPath, toolIn, kronaPath, pTreePath = init_argv()
	sigma_visualization(toolPath, toolIn, kronaPath, pTreePath)
