import os, glob, sys
def sigma_visualization(toolPath, toolIn, kronaPath):
    command = './' + toolPath + ' ' + toolIn
    print command
    os.system(command)
    kronaIn = []
    kronaIn.append(toolIn+'_krona1')
    kronaIn.append(toolIn+'_krona2')
    for k in range(len(kronaIn)):
        command = kronaPath + ' -o ' + kronaIn[k] + '.html ' + kronaIn[k]
        print command
        os.system(command)

def init_argv():
    toolPath = ""
    toolIn = ""
    kronaPath = ""
    
    for i in range(len(sys.argv)):
        if sys.argv[i] == "-kp" : kronaPath  = sys.argv[i+1]
        if sys.argv[i] == "-tp": toolPath = sys.argv[i+1]
        if sys.argv[i] == "-ti": toolIn = sys.argv[i+1]
    return toolPath, toolIn, kronaPath

if __name__ == "__main__":
    toolPath, toolIn, kronaPath = init_argv()
    sigma_visualization(toolPath, toolIn, kronaPath)
