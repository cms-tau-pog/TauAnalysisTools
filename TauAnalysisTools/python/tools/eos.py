
import datetime
import os
import shlex
import subprocess
import sys
import time

executable_eos = '/afs/cern.ch/project/eos/installation/cms/bin/eos.select'

def runCommand(commandLine):
    #sys.stdout.write("%s\n" % commandLine)
    args = shlex.split(commandLine)
    retVal = subprocess.Popen(args, stdout = subprocess.PIPE)
    return retVal

def lsl(file_or_path):
    '''
    List EOS file/directory content, returning the information found in 'eos ls -l'.
    The output is a list of dictionaries with the following entries:
        permissions
        file
        modified
        size (in bytes)
    An exception of type IOError will be raised in case file/directory does not exist.
    '''

    directory = os.path.dirname(file_or_path)
    ls_command = runCommand('%s ls -l %s' % (executable_eos, file_or_path))

    stdout, stderr = ls_command.communicate()
    #print "stdout = ", stdout
    status = ls_command.returncode
    #print "status = ", status
    if status != 0:
        raise IOError("File/path = %s does not exist !!" % file_or_path)

    retVal = []
    for line in stdout.splitlines():
        fields = line.split()
        if len(fields) < 8:
            continue
        file_info = {
            'permissions' : fields[0],
            'size' : int(fields[4]),
            'file' : fields[8]
        }
        time_stamp = " ".join(fields[5:8])
        # CV: value of field[7] may be in format "hour:minute" or "year".
        #     if number contains ":" it means that value specifies hour and minute when file/directory was created
        #      and file/directory was created this year.
        if time_stamp.find(':') != -1:
            file_info['time'] = time.strptime(
                time_stamp + " " + str(datetime.datetime.now().year),
                "%b %d %H:%M %Y")
        else:
            file_info['time'] = time.strptime(time_stamp, "%b %d %Y")
        file_info['path'] = os.path.join(directory, file_info['file'])
        #print "file_info = " % file_info
        retVal.append(file_info)
    return retVal

def mkdir(path):
    '''
    Create new EOS directory.
    An exception of type RuntimeError will be raised in case directory does already exist.
    '''
    pathExists = True
    try:
        lsl(path)
    except IOError:
        pathExists = False
    if pathExists:
        raise RuntimeError("Path %s does already exist !!" % path)

    mkdir_command = runCommand('%s mkdir %s' % (executable_eos, path))
    status = mkdir_command.returncode
    #print "status = ", status
    if status != 0:
        raise IOError("Impossible to create path = %s !!" % path)

def cp(inputFileNames, outputFilePath):
    """
    Copy the inFiles into the outDir
    """
    for inputFileName in inputFileNames:
        runCommand('% cp %s %s' % (executable_eos, inputFileName, os.path.join(outputFilePath, os.path.basename(inputFileName))))
    return 1

