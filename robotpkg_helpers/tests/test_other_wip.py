#!/usr/bin/python3
import os
from robotpkg_helpers import RobotpkgTests, build_test_rc_robotpkg_vars

# This script assumes that a directory in your folder:
# $HOME/devel-src/distfiles
# contains all the distribution files needed to recompile robotpkg.
#
# Robotpkg is extracted here from the repository located at:
# git@gepgitlab.laas.fr:user/robotpkg-wip.git wip
#
# It then rebuild completly robotpkg by extracting the sources in the folder:
# $HOME/devel-src/robotpkg-test-rc/robotpkg
# Then everything is compiled and installed in:
# $HOME/devel-src/robotpkg-test-rc/install
#

robotpkg_vars = build_test_rc_robotpkg_vars()

wip_repository='https://github.com/nim65s/robotpkg-wip.git wip'

arpg_test_dist_files=RobotpkgTests("/integration_tests/robotpkg-test-rc")
arpg_test_dist_files.perform_test_rc(wip_repository=wip_repository)
arpg_test_dist_files.compile_package('talos-dev')

