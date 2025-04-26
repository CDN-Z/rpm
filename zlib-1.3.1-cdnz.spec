Name:               cdnz-zlib
Version:            1.3.1
Release:            1%{?dist}
Summary:            The zlib compression library for CDNZ
Group:              System Environment/Libraries

# /contrib/dotzlib/ have Boost license
License:            zlib and Boost
URL:                https://www.zlib.net/
Source0:            https://www.zlib.net/zlib-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:      libtool
AutoReqProv:        no

%define zlib_prefix     /usr/local/cdnz/zlib


%description
The zlib compression library for use by CDNZ ONLY

%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/zlib-%{version}"; \
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

Summary:            Development files for CDNZ's zlib library
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}


%description devel
Provides C header and static library for CDNZ's zlib library.


%prep
# Always download a fresh copy of the source
# Download source if not present
if [ ! -f %{_sourcedir}/zlib-%{version}.tar.gz ]; then
    wget -O %{_sourcedir}/zlib-%{version}.tar.gz %{SOURCE0}
fi
%setup -q -n zlib-%{version}

%build
./configure --prefix=%{zlib_prefix}
make -j`nproc` CFLAGS='-O3 -fPIC -D_LARGEFILE64_SOURCE=1 -DHAVE_HIDDEN -g3' \
    SFLAGS='-O3 -fPIC -D_LARGEFILE64_SOURCE=1 -DHAVE_HIDDEN -g3' \
    > /dev/stderr

%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}/%{zlib_prefix}/share
rm -f  %{buildroot}/%{zlib_prefix}/lib/*.la
rm -rf %{buildroot}/%{zlib_prefix}/lib/pkgconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)

%dir %{zlib_prefix}
%dir %{zlib_prefix}/lib
%attr(0755,root,root) %{zlib_prefix}/lib/libz.so*

%files devel
%defattr(-,root,root,-)

%dir %{zlib_prefix}/include
%{zlib_prefix}/lib/*.a
%{zlib_prefix}/include/zlib.h
%{zlib_prefix}/include/zconf.h