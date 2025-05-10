#!/bin/bash

dnf update -y
dnf install -y rpm-build rpmdevtools dnf-utils createrepo yum-utils wget git \
    gcc gcc-c++ make zlib-devel pcre-devel openssl-devel libxml2-devel \
    libxslt-devel gd-devel perl-devel pam-devel perl-core lksctp-tools-devel \
    vim libtool readline-devel cmake