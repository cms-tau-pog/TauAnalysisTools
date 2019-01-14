# def createFilePath(filePath):
#    import TauAnalysis.Configuration.tools.eos as eos
#    try:
#        eos.lsl(filePath)
#    except IOError:
#        print "filePath = %s does not yet exist, creating it." % filePath
#        eos.mkdir(filePath)
#        time.sleep(3)
#    eos.chmod(filePath, 777)

import subprocess

def runcommand(commandline):
    """Run and print a specific command."""
    print(commandline)
    subprocess.call(commandline, shell=True)