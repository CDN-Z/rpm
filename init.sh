#!/bin/bash
# Script to build and install

dnf update -y
dnf install -y rpm-build rpmdevtools dnf-utils createrepo yum-utils wget git \
    gcc gcc-c++ make zlib-devel pcre-devel openssl-devel libxml2-devel \
    libxslt-devel gd-devel perl-devel pam-devel perl-core lksctp-tools-devel \
    vim

# Install openSSL 3.5
install_openssl() {
    # Exit on any error
    set -e

    # Define variables
    local OPENSSL_VERSION="3.5.0"
    local OPENSSL_TAR="openssl-${OPENSSL_VERSION}.tar.gz"
    local OPENSSL_URL="https://github.com/openssl/openssl/releases/download/openssl-${OPENSSL_VERSION}/${OPENSSL_TAR}"
    local INSTALL_DIR="/usr/local/openssl"

    # Download OpenSSL
    echo "Downloading OpenSSL ${OPENSSL_VERSION}..."
    curl -L -o ${OPENSSL_TAR} ${OPENSSL_URL}
    echo "Extracting ${OPENSSL_TAR}..."
    tar -xzf ${OPENSSL_TAR}

    # Change to extracted directory
    cd openssl-${OPENSSL_VERSION}

    # Configure OpenSSL
    echo "Configuring OpenSSL..."
    ./config --prefix=${INSTALL_DIR} --openssldir=${INSTALL_DIR} shared zlib sctp

    # Compile and install
    echo "Compiling and installing OpenSSL..."
    make -j$(nproc)
    make install

    # Update library path
    echo "Updating library path..."
    ldconfig
    echo "${INSTALL_DIR}/lib64" | tee /etc/ld.so.conf.d/openssl.conf
    ldconfig
    rm -rf /usr/bin/openssl
    ln -s /usr/local/openssl/bin/openssl /usr/bin/openssl

    # Clean up
    echo "Cleaning up..."
    cd ..
    rm -rf openssl-${OPENSSL_VERSION} ${OPENSSL_TAR}

    # Verify installation
    echo "Verifying OpenSSL installation..."
    ${INSTALL_DIR}/bin/openssl version
    # Verify SCTP support
    ${INSTALL_DIR}/bin/openssl s_client -help 2>&1 | grep -q sctp && echo "SCTP support enabled" || echo "SCTP support not enabled"

    echo "OpenSSL ${OPENSSL_VERSION} installed successfully in ${INSTALL_DIR}"

}

install_luajit() {
    # Exit on any error
    set -e

    # Define variables
    local LUAJIT_VERSION="2.1-20250117"
    local LUAJIT_TAR="v${LUAJIT_VERSION}.tar.gz"
    local LUAJIT_URL="https://github.com/openresty/luajit2/archive/refs/tags/${LUAJIT_TAR}"
    local INSTALL_DIR="/usr/local/luajit"
    local SRC_DIR="/usr/local/src/luajit"

    # Create source directory
    echo "Creating source directory..."
    mkdir -p ${SRC_DIR}
    cd ${SRC_DIR}

    # Download LuaJITi
    echo "Downloading LuaJIT ${LUAJIT_VERSION}..."
    curl -L -o ${LUAJIT_TAR} ${LUAJIT_URL}

    echo "Extracting ${LUAJIT_TAR}..."
    tar -xzf ${LUAJIT_TAR}

    cd luajit2-${LUAJIT_VERSION}

    echo "Compiling and installing LuaJIT..."
    make -j$(nproc) PREFIX=${INSTALL_DIR}
    make install PREFIX=${INSTALL_DIR}

    # Update library path
    echo "Updating library path..."
    ldconfig
    echo "${INSTALL_DIR}/lib" | tee /etc/ld.so.conf.d/luajit.conf
    ldconfig

    # Create symlink for luajit executable (optional, for convenience)
    ln -sf ${INSTALL_DIR}/bin/luajit-${LUAJIT_VERSION} /usr/local/bin/luajit
}

download_github_repo() {
  local branch_or_commit_opt=$1
  local branch_or_commit=$2
  local user_repo=$3

  local user=${user_repo%%/*}
  local repo=${user_repo##*/}

  if [ -d $repo ]; then
    rm -rf ${repo}
  fi

  local commit
  case "$branch_or_commit_opt" in
  -b)
    git clone --depth 1 -b ${branch_or_commit} --recurse-submodules https://github.com/${user}/${repo}.git > /dev/null 2>&1
    commit=$(cd ${repo} && git rev-parse HEAD)
    rm -rf ${repo}/.git
    ;;
  -c)
    mkdir ${repo}
    curl -sSL https://github.com/$user/$repo/archive/${commit}.tar.gz | tar zxf - --strip-component 1 -C ${repo}
    commit=${branch_or_commit}
    ;;
  esac

  tar cf - ${repo} | gzip -9 > SOURCES/${repo}.tar.gz
  rm -rf ${repo}
  echo "%define ${repo//-/_}_commit $commit"
}

