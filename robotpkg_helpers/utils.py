import os
import subprocess
from .analyze_computer import AnalyzeComputer

    
def add_colors(anObject):
    """ Initialize colors for beautification
    
    The following variables are available:
    REG, GREEN, PURPLE, NC (no color)
    """
    anObject.RED =  '\033[0;31m'
    anObject.GREEN= '\033[0;32m'
    anObject.PURPLE='\033[0;35m'
    anObject.NC =   '\033[0m'

def execute_capture_output(bashCommand,filename,lenv,debug=0):
    """ Execute baschCommand 
    
    Keyword arguments:
    bashCommand -- the bashCommand to be run in a bash script
    
    It returns a list of binary string that can be iterate 
    and decode.
    
    """
    # TODO: Handle error
    if debug>3:
        print("execute bash command: "+bashCommand)
    with open(filename,'w') as output:
        process = subprocess.check_call(bashCommand.split(),
                    stdout=output,
                    env=lenv)
    return ""

def execute(bashCommand, lenv, debug=0):
    """ Execute baschCommand 
    
    Keyword arguments:
    bashCommand -- the bashCommand to be run in a bash script
    
    It returns a list of binary string that can be iterate 
    and decode.
    
    """
    # TODO: Handle error
    if debug>3:
        print("execute bash command: "+bashCommand)
        print("env to run the command:")
        print(lenv)
    process = subprocess.Popen(bashCommand.split(),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               env=lenv)
    outputdata, error = process.communicate()
    p_status = process.returncode
    if debug>3:
        for stdout_line in outputdata.splitlines():
            print(stdout_line.decode('utf-8'))
    return outputdata,error,p_status

def execute_call(bashCommand, debug=0):
    """ Execute baschCommand 
        
    Keyword arguments:
    bashCommand -- the bashCommand to be run in a bash script
    
    It returns a list of binary string that can be iterate 
    and decode.
    
    """
    if debug>3:
        print("execute bash command: "+bashCommand)
    return subprocess.call(bashCommand,shell=True)

# def add_robotpkg_mng_variables(anObject,
#                                ROBOTPKG_MNG_ROOT=None,
#                                ROBOTPKG_MNG_BASE=None,
#                                sub_ramfs_mnt_pt='robotpkg-test-rc',
#                                sub_arch_dist_files='arch_distfiles',
#                                sub_archives='archives'):
#     """ This function adds robotpkg_mng_vars to the object anObject based on ROBOTPKG_MNG_ROOT
#     if provided. 
#     The keys of the dictionnary are build the following way
#     - 'ROOT' = ROBOTPKG_MNG_ROOT
#     - 'ARCH_DISTFILES' = ROBOTPKG_MNG_ROOT/sub_arch_dist_files
#     - 'RAMFS_MNT_PT' = ROBOTPKG_MNG_ROOT/sub_ramfs_mnt_pt
#     - 'ROBOTPKG_ROOT' = RAMFS_MNT_PT
#     - 'ARCHIVES' = ROBOTPKG_MNG_ROOT/sub_archives
#     if ROBOTPKG_MNG_BASE==None
#        - 'ROBOTPKG_BASE' = ROBOTPKG_MNG_ROOT/install
#     else
#        - 'BOBOTPKG_BASE' = ROBOTPKG_MNG_BASE

#     - 'ROBOTPKG_SRC' = ROBOTPKG_MNG_ROOT/robotpkg

#     All of this is done for intermediate build when working on release candidates
#     and speed up deployment tests.
    
#     TODO: Test over a solution an integrative solution with dockerfile and 
#     intermediate binary build.
#     """
#     if ROBOTPKG_MNG_ROOT==None:
#         anObject.ROBOTPKG_MNG_ROOT='/integration_tests'
#     else:
#         anObject.ROBOTPKG_MNG_ROOT=ROBOTPKG_MNG_ROOT

#     anObject.robotpkg_mng_vars={}
#     anObject.robotpkg_mng_vars['ROOT'] = anObject.ROBOTPKG_MNG_ROOT
#     anObject.robotpkg_mng_vars['ARCH_DISTFILES']=anObject.robotpkg_mng_vars['ROOT']+'/'+sub_arch_dist_files
#     anObject.robotpkg_mng_vars['RAMFS_MNT_PT']=anObject.robotpkg_mng_vars['ROOT']+'/'+sub_ramfs_mnt_pt
#     anObject.robotpkg_mng_vars['ROBOTPKG_ROOT']=anObject.robotpkg_mng_vars['RAMFS_MNT_PT']
#     anObject.robotpkg_mng_vars['ARCHIVES']=anObject.robotpkg_mng_vars['ROOT']+'/'+sub_archives
#     if ROBOTPKG_MNG_BASE!=None:
#         anObject.robotpkg_mng_vars['ROBOTPKG_BASE']=ROBOTPKG_MNG_BASE
#     else:anObject.robotpkg_mng_vars['ROBOTPKG_BASE']
#         anObject.robotpkg_mng_vars['ROBOTPKG_BASE']=anObject.robotpkg_mng_vars['RAMFS_MNT_PT']+'/install'
#     anObject.robotpkg_mng_vars['ROBOTPKG_SRC']=anObject.robotpkg_mng_vars['RAMFS_MNT_PT']+'/robotpkg'


def init_environment_variables(anObject):
    """ Populate the object with the environment variables.
    
    Specifies the environment when starting bash commands
    """
    # Create an object to analyze the computer
    an_analyze_computer = AnalyzeComputer()

    anObject.ROBOTPKG_BASE = anObject.robotpkg_mng_vars['robotpkg_mng_base']
    anObject.env = os.environ.copy()
    ROBOTPKG_BASE = anObject.ROBOTPKG_BASE
    anObject.env["ROBOTPKG_BASE"] = ROBOTPKG_BASE
    # Imposes bash as the shell
    anObject.env["SHELL"] = "/usr/bin/bash"
    # For binaries
    anObject.env["PATH"] = ROBOTPKG_BASE+'/sbin:' + \
                       ROBOTPKG_BASE+'/bin:'+ \
                       '/opt/ros/'+an_analyze_computer.ros_distrib + '/bin:' + \
                       anObject.env["PATH"]
    
    # For libraries
    prev_LD_LIBRARY_PATH=''
    if "LD_LIBRARY_PATH" in anObject.env:
        prev_LD_LIBRARY_PATH = anObject.env["LD_LIBRARY_PATH"]
    anObject.env["LD_LIBRARY_PATH"] = ROBOTPKG_BASE+'/lib:' \
        +ROBOTPKG_BASE+'/lib/plugin:' \
        +ROBOTPKG_BASE+'/lib64:' \
        +prev_LD_LIBRARY_PATH
        
    # For python
    prev_PYTHONPATH=''
    if "PYTHONPATH" in anObject.env:
        prev_PYTHONPATH = anObject.env["PYTHONPATH"]
    anObject.env["PYTHONPATH"]=ROBOTPKG_BASE+'/lib/python2.7/site-packages:' \
        +ROBOTPKG_BASE+'/lib/python2.7/dist-packages:' \
        +prev_PYTHONPATH
        
    # For pkgconfig
    prev_PKG_CONFIG_PATH=''
    if "PKG_CONFIG_PATH" in anObject.env:
        prev_PKG_CONFIG_PATH = anObject.env["PKG_CONFIG_PATH"]

    anObject.env["PKG_CONFIG_PATH"]=ROBOTPKG_BASE+'/lib/pkgconfig:' \
        +prev_PKG_CONFIG_PATH
        
    # For ros packages
    prev_ROS_PACKAGE_PATH=''
    if "ROS_PACKAGE_PATH" in anObject.env:
        prev_ROS_PACKAGE_PATH = anObject.env["ROS_PACKAGE_PATH"]
        
    anObject.env["ROS_PACKAGE_PATH"]=ROBOTPKG_BASE+'/share:' \
        +ROBOTPKG_BASE+'/stacks:' \
        +prev_ROS_PACKAGE_PATH
        
    # For cmake
    prev_CMAKE_PREFIX_PATH=''
    if "CMAKE_PREFIX_PATH" in anObject.env:
        prev_CMAKE_PREFIX_PATH = anObject.env["CMAKE_PREFIX_PATH"]
            
    anObject.env["CMAKE_PREFIX_PATH"]=ROBOTPKG_BASE+':'+prev_CMAKE_PREFIX_PATH
