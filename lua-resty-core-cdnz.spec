Name:       lua-resty-core
Version:    1.0.0
Release:    1%{?dist}
Summary:    Install lua-resty-core for CDNZ
License:    BSD
URL:        https://github.com/CDN-Z/lua-resty-core

Source0:    https://github.com/CDN-Z/lua-resty-core/archive/refs/tags/v%{version}.tar.gz

BuildRequires: lua-filesystem

%define prefix     /usr/local/cdnz

# For Rocky Linux 9.3
%if 0%{?rhel} >= 9
%global debug_package %{nil}
%global _enable_debug_package 0
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}
%endif

%description
lua-resty-core is a library for OpenResty and Nginx Lua module, providing core functionalities.

%prep
%setup -q -n %{name}-%{version}

%build
# No compilation required, as lua-resty-core is a pure Lua module

%install
make install

%clean
rm -rf %{buildroot}
