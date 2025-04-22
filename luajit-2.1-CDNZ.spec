%define luajit_version 2.1
%define luajit_date_version 20250117

Name:           cdnz-luajit
Version:        %{luajit_version}.%{luajit_date_version}
Release:        1%{?dist}
Summary:        Just-In-Time Compiler for Lua (OpenResty branch)
License:        MIT
URL:            https://github.com/openresty/luajit2
Source0:        https://github.com/openresty/luajit2/archive/v%{luajit_version}-%{luajit_date_version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%define luajit_prefix /usr/local/cdnz/luajit2.1

# For Rocky Linux 9.3
%if 0%{?rhel} >= 9
%global debug_package %{nil}
%global _enable_debug_package 0
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}
%endif

%description
LuaJIT is a Just-In-Time Compiler for the Lua programming language.
This package contains the OpenResty branch of LuaJIT with additional features.

%package devel
Summary:        Development files for LuaJIT
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains development files for LuaJIT.

%prep
# Download source if not present
if [ ! -f %{_sourcedir}/luajit2-%{luajit_version}-%{luajit_date_version}.tar.gz ]; then
    wget -O %{_sourcedir}/luajit2-%{luajit_version}-%{luajit_date_version}.tar.gz %{SOURCE0}
fi
%setup -q -n luajit2-%{luajit_version}-%{luajit_date_version}

%build
# Determine number of parallel jobs
ncpus=`nproc`
if [ "$ncpus" -gt 16 ]; then
    ncpus=16
fi

# Build with optimizations, verbose output, and specific target architecture
make -j$ncpus amalg Q= E=@: PREFIX=%{luajit_prefix} TARGET_STRIP=: \
     CFLAGS="%{optflags}" \
     XCFLAGS="-DLUAJIT_ENABLE_LUA52COMPAT -DLUAJIT_NUMMODE=2" \
     TARGET_CFLAGS="%{optflags}" \
     linux-x86_64

%install
rm -rf %{buildroot}

# Install LuaJIT
make install PREFIX=%{luajit_prefix} DESTDIR=%{buildroot}

# Fix permissions
chmod 0755 %{buildroot}%{luajit_prefix}/lib/*.so*

# Create documentation directory
mkdir -p _tmp_html
cp -a doc _tmp_html/html

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%license COPYRIGHT
%doc README
%dir %{luajit_prefix}
%dir %{luajit_prefix}/bin
%dir %{luajit_prefix}/lib
%dir %{luajit_prefix}/share
%{luajit_prefix}/bin/luajit
%{luajit_prefix}/bin/luajit-%{luajit_version}
%{luajit_prefix}/lib/libluajit*.so.*
%{luajit_prefix}/share/luajit-%{luajit_version}
%{luajit_prefix}/share/man

%files devel
%defattr(-,root,root,-)
%doc _tmp_html/html/
%dir %{luajit_prefix}/include
%{luajit_prefix}/include/*
%{luajit_prefix}/lib/libluajit*.so
%{luajit_prefix}/lib/pkgconfig