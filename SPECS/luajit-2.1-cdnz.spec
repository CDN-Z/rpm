%define luajit_version 2.1
%define luajit_date_version 20250117
%define luajit_bin_version 2.1
%define cdnz_prefix /usr/local/cdnz
%define luajit_prefix %{cdnz_prefix}/luajit2.1

Name:           cdnz-luajit
Version:        %{luajit_version}.%{luajit_date_version}
Release:        1%{?dist}
Summary:        Just-In-Time Compiler for Lua for CDNZ
License:        MIT
URL:            http://luajit.org/
Source0:        https://github.com/openresty/luajit2/archive/v%{luajit_version}-%{luajit_date_version}.tar.gz

# For Rocky Linux 9.3
%if 0%{?rhel} >= 9
%global debug_package %{nil}
%global _enable_debug_package 0
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}
%endif

%description
LuaJIT implements the full set of language features defined by Lua 5.1.
The virtual machine (VM) is API- and ABI-compatible to the standard
Lua interpreter and can be deployed as a drop-in replacement.

This package uses the OpenResty's fork of LuaJIT 2.
https://github.com/openresty/luajit2

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains development files for %{name}.

%prep
%setup -q -n luajit2-%{luajit_version}-%{luajit_date_version}
echo '#!/bin/sh' > ./configure
chmod +x ./configure

# preserve timestamps
sed -i -e '/install -m/s/-m/-p -m/' Makefile

%build
# Build with optimizations and necessary flags
make amalg Q= E=@: PREFIX=%{luajit_prefix} TARGET_STRIP=: \
     CFLAGS="%{optflags} -fno-lto" \
     LDFLAGS="-ldl -Wl,-E" \
     XCFLAGS="-DLUAJIT_ENABLE_LUA52COMPAT -DLUAJIT_NUMMODE=2"

%install
rm -rf %{buildroot}

# Install with custom prefix
make install PREFIX=%{luajit_prefix} DESTDIR=%{buildroot}

# Create versioned symlinks
ln -sf luajit %{buildroot}%{luajit_prefix}/bin/luajit-%{luajit_bin_version}

# Fix permissions
chmod 0755 %{buildroot}%{luajit_prefix}/lib/*.so*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license COPYRIGHT
%doc README
%dir %{luajit_prefix}
%dir %{luajit_prefix}/bin
%dir %{luajit_prefix}/lib
%dir %{luajit_prefix}/share
%{luajit_prefix}/bin/luajit
%{luajit_prefix}/bin/luajit-%{luajit_bin_version}
%{luajit_prefix}/bin/luajit-%{luajit_bin_version}.*
%{luajit_prefix}/lib/libluajit*.so.*
%{luajit_prefix}/share/luajit-%{luajit_bin_version}/
%{luajit_prefix}/share/man/man1/luajit.1

%files devel
%{luajit_prefix}/include/luajit-%{luajit_bin_version}/
%{luajit_prefix}/lib/libluajit*.so
%{luajit_prefix}/lib/libluajit*.a
%{luajit_prefix}/lib/pkgconfig/*.pc