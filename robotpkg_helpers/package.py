import os
import re

class RobotpkgPackage:
    
    def __init__(self,name,path,group,subgroup=None,debug=0):
        self.name=name
        self.path=path
        self.group=group
        self.debug=debug
        self.subgroup=subgroup

    def display(self):
        """ Display the information extracted from robotpkg
        """
        print("Name: "+self.name)
        print("Path: "+self.path)
        print("Group: "+self.group)
        if not self.subgroup==None:
            print("Subgroup: "+self.subgroup)
        
        if hasattr(self,'rpkg_name'):
            if not len(self.rpkg_name)==0:
                print("Robotpkg name: ")
                print(self.rpkg_name)

        if hasattr(self,'org_name'):                
            if not len(self.org_name)==0:
                print("Organization: ")
                print(self.org_name)
                
        if hasattr(self,'master_repository'):
            if not len(self.master_repository)==0:
                print("Master repository: ")
                print(self.master_repository)

        if hasattr(self,'version'):
            if not len(self.version)==0:
                print("Version: ")
                print(self.version)

        if hasattr(self,'includes_depend'):
            print("Dependencies in Makefile with depend.mk:")
            print(self.includes_depend)

        if hasattr(self,'includes_mk'):
            print("Dependencies in Makefile in mk group:")
            print(self.includes_mk)

        if hasattr(self,'depend_mk_system_pkg'):
            if not len(self.depend_mk_system_pkg)==0:
                print("Depend SYSTEM in depend.mk:")
                print(self.depend_mk_system_pkg)

        if hasattr(self,'tree_of_includes_os'):
            print("tree_of_includes_os:")
            print(self.tree_of_includes_os)

        if hasattr(self,'tree_of_includes_dep'):
            print("tree_of_includes_dep:")
            print(self.tree_of_includes_dep)
            
        
    def analyze_makefile(self,make_content):
        """ This methods analyzes the contents of the string make_content.
        The string is the contents of the Makefile file inside the package directory.
    
        Right now it populates the attributes:
        rpkg_name: The name of the package as PKGNAME (if provided)
        org_name: The name of the organization in charge of the package (if provided)
        license: The name of the package's license (if provided)
        master_repository: Link to the repository of the package (if provided)
        version: Version of the package (necessary)
        includes_depend_mk: list of packages provided by robotpkg 
        includes_mk. list of  packages needed for the current package but provided by the system.
        """

        # Search for NAME
        self.rpkg_name = re.findall("PKGNAME\s*=\s*([0-9azA-Z-]+)",make_content)
        if self.debug>3:
            print("analyze_makefile for " + self.name)
            if not len(self.rpkg_name)==0 :
                print("analyze_makefile: " + self.rpkg_name[0])

        # Search for ORG
        self.org_name = re.findall("ORG\s*=\s*([azA-Z-]+)",make_content)
        if self.debug>3:
            if not len(self.org_name)==0:
                print("analyze_makefile: " + self.org_name[0])

        # Search for LICENSE
        self.license = re.findall("LICENSE\s*=\s*([a-zA-Z0-9\-]+)",make_content)
        if self.debug>3:
            if not len(self.license)==0:
                print("analyze_makefile license: " + self.license[0])

        # Search for MASTER_REPOSITORY
        self.master_repository = re.findall("MASTER_REPOSITORY\s*=\s*([a-zA-Z0-9\-\${}_]+)",make_content)
        if self.debug>3:
            if not len(self.master_repository)==0:
                print("analyze_makefile master_repository: " + self.master_repository[0])

        # Search for VERSION
        self.version = re.findall("VERSION\s*=\s*([a-zA-Z0-9\-.]+)",make_content)
        if self.debug>3:
            if not len(self.version)==0:
                print("analyze_makefile version: " + self.version[0])

        # Search for include
        self.includes_depend = re.findall("include\s*../../([0-9a-zA-Z-]+)/([0-9a-zA-Z-]+)/depend.mk",make_content)
        
        # Search for mk
        self.includes_mk = re.findall("include\s*../../mk/([0-9a-zA-Z-]+)/([0-9a-zA-Z-]+).mk",make_content)

    def read_makefile(self):
        # Keep current directory.
        current_path=os.getcwd()

        # Reading Makefile
        os.chdir(self.path)
        if os.path.isfile("Makefile"):
            with open("Makefile",mode='r',encoding='utf-8') as f_cmakelists:
                make_content = f_cmakelists.read()
                self.analyze_makefile(make_content)
        
        # Going back to where we were
        os.chdir(current_path)
        
    def analyze_depend_mk(self,depend_mk_content):
        """ This methods analyzes the contents of the string depend_mk_content.
        The string is the contents of the depend.mk file inside the package directory.
    
        Right now it populates one list called depend_mk_system_pkg. It gives
        the system packages needed for the current package.
        """
        # Search for SYSTEM_PKG
        self.depend_mk_system_pkg = re.findall("SYSTEM_PKG\.Ubuntu\.([0-9a-zA-Z\-]+)\s*=\s*([0-9a-zA-Z\-]+)",depend_mk_content)

        if self.debug>3:
            print("depend_mk_system_pkg: " + self.name)
            print(self.depend_mk_system_pkg)
        
        if len(self.depend_mk_system_pkg)==0:
            self.depend_mk_system_pkg = re.findall("SYSTEM_PKG\.Debian\.([0-9a-zA-Z\-]+)\s*=\s*([0-9a-zA-Z\-]+)",depend_mk_content)
            
        if self.debug>3:
            print(self.depend_mk_system_pkg)

    def read_depend_mk(self):
        """ This methods open the file depend.mk inside a package directory.
    
        Right it populates the packages with one variable depend_mk_system_pkg which are
        the system packages needed for this package.
        """

        # Keep current directory.
        current_path=os.getcwd()

        # Reading Makefile
        os.chdir(self.path)
        if os.path.isfile("depend.mk"):
            with open("depend.mk",mode='r',encoding='utf-8') as f_depend_mk:
                depend_mk_content = f_depend_mk.read()
                self.analyze_depend_mk(depend_mk_content)
        
        # Going back to where we were
        os.chdir(current_path)

    def read_package_info(self):
        self.read_makefile()
        self.read_depend_mk()
        
    