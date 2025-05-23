Name:               cdnz-openssl3
Version:            3.5.0
Release:            1%{?dist}
Summary:            OpenSSL library for CDNZ

Group:              Development/Libraries

# https://www.openssl.org/source/license.html
License:            OpenSSL
URL:                https://www.openssl.org/
Source0:            https://github.com/openssl/openssl/releases/download/openssl-%{version}/openssl-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc, make, perl
BuildRequires:      cdnz-zlib-devel >= 1.2.11
Requires:           cdnz-zlib >= 1.2.11

AutoReqProv:        no
%define openssl_prefix      /usr/local/cdnz/openssl3
%define zlib_prefix         /usr/local/cdnz/zlib
%global _default_patch_fuzz 1


%description
This OpenSSL library build is specifically for CDNZ uses. It may contain
custom patches from CDNZ.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/openssl-%{version}"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/tmp"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/builddir"; \
%{nil}

%endif

# For Rocky Linux 9.3
%if 0%{?rhel} >= 9
%global debug_package %{nil}
%global _enable_debug_package 0
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}
%endif

%package devel

Summary:            Development files for CDNZ's OpenSSL library
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}


%description devel
Provides C header and static library for CDNZ's OpenSSL library.

%prep
# Always download a fresh copy of the source
# Download source if not present
if [ ! -f %{_sourcedir}/openssl-%{version}.tar.gz ]; then
    wget -O %{_sourcedir}/openssl-%{version}.tar.gz %{SOURCE0}
fi
%setup -q -n openssl-%{version}

%build
./config \
    no-tests no-docs \
    shared zlib -g \
    --prefix=%{openssl_prefix} \
    --libdir=lib \
    enable-camellia enable-seed enable-rfc3779 \
    enable-cms enable-md2 enable-rc5 \
    enable-weak-ssl-ciphers \
    enable-ssl3 enable-ssl3-method \
    enable-md2 enable-ktls enable-fips\
    -I%{zlib_prefix}/include \
    -L%{zlib_prefix}/lib \
    -Wl,-rpath,%{zlib_prefix}/lib:%{openssl_prefix}/lib

ncpus=`nproc`
if [ "$ncpus" -gt 16 ]; then
    ncpus=16
fi

%install
make install_sw DESTDIR=%{buildroot}

chmod 0755 %{buildroot}%{openssl_prefix}/lib/*.so*
chmod 0755 %{buildroot}%{openssl_prefix}/lib/*/*.so*

rm -rf %{buildroot}%{openssl_prefix}/bin/c_rehash

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)

%dir %{openssl_prefix}
%dir %{openssl_prefix}/bin
%dir %{openssl_prefix}/lib
%dir %{openssl_prefix}/lib/engines-3
%dir %{openssl_prefix}/lib/ossl-modules
%attr(0755,root,root) %{openssl_prefix}/bin/openssl
%{openssl_prefix}/lib/libcrypto.so.3
%{openssl_prefix}/lib/libssl.so.3
%{openssl_prefix}/lib/libcrypto.so
%{openssl_prefix}/lib/libssl.so
%{openssl_prefix}/lib/engines-3/*.so
%{openssl_prefix}/lib/ossl-modules/*.so


%files devel
%defattr(-,root,root,-)

%dir %{openssl_prefix}/include
%{openssl_prefix}/include/*
%{openssl_prefix}/lib/*.a
%{openssl_prefix}/lib/pkgconfig/*.pc
%{openssl_prefix}/lib/cmake/OpenSSL/OpenSSLConfig.cmake
%{openssl_prefix}/lib/cmake/OpenSSL/OpenSSLConfigVersion.cmake
