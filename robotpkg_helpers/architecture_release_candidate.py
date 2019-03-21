import os
import sys
import json
from .package_release_candidate import RobotpkgPkgReleaseCandidate
from .package_release_candidate import display_description

class RobotpkgArchitectureReleaseCandidate:

    def __init__(self, json_filename=None):
        self.data={}
        self.data['ssh_git_openrobots']=False
        # Check if a JSON file has been provided
        if json_filename!=None:
            self.load_rc(json_filename)

    def default_init(self):
        if self.data['ssh_git_openrobots']:
            self.data['repo_robotpkg_main'] = \
                'https://git.openrobots.org/robots/robotpkg.git'
            self.data['repo_robotpkg_wip'] = \
                'ssh://git@git.openrobots.org/robots/robotpkg/robotpkg-wip'
        else:
            self.data['repo_robotpkg_main'] = \
                'https://git.openrobots.org/robots/robotpkg.git'
            self.data['repo_robotpkg_wip'] = \
                'https://git.openrobots.org/robots/robotpkg/robotpkg-wip.git'
        self.data['rc_pkgs']={}
        self.data['robotpkg_mng_root']='/integration_tests'
        self.data['ramfs_mnt_pt']='robotpkg-test-rc'
        self.data['arch_dist_files']='arch_distfiles'
        self.data['archives']='archives'

    def display(self):
        print("git url - robotpkg:")
        print("  "+self.data['repo_robotpkg_main'])
        print("git url - robotpkg wip:")
        print("  "+self.data['repo_robotpkg_wip'])
        for name,desc_package in self.data['rc_pkgs'].items():
            display_description(desc_package)
        
    def load_rc(self,filename):
        if os.path.isfile(filename):
            with open(filename) as json_filename:
                self.data = json.load(json_filename)
        else:
            print(filename + " does not exists")
        
    def save_rc(self,filename):
        f=open(filename,'w')
        json.dump(self.data,f)
        f.close()
        