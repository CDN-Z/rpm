FROM rockylinux:9.3

# Install dependencies
RUN dnf update -y

RUN dnf install -y rpm-build rpmdevtools dnf-utils createrepo yum-utils wget git \
        gcc gcc-c++ make zlib-devel pcre-devel openssl-devel libxml2-devel \
        libxslt-devel gd-devel perl-devel pam-devel perl-core lksctp-tools-devel \
        vim libtool readline-devel cmake chrpath

RUN rpmdev-setuptree

# Set up the entrypoint script
WORKDIR /root/rpmbuild

COPY SPECS/ ./SPECS/
COPY SOURCES/ ./SOURCES/

COPY entrypoint.sh ./
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["/bin/bash", "/root/rpmbuild/entrypoint.sh"]