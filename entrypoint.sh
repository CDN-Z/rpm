#!/bin/sh

spectool -g -R /root/rpmbuild/SPECS/ccache-cdnz.spec
# Build the RPMs
rpmbuild -ba /root/rpmbuild/SPECS/ccache-cdnz.spec
