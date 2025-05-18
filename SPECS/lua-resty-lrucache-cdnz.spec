Name:       lua-resty-lrucache
Version:    1.0.0
Release:    1%{?dist}
Summary:    Install lua-resty-lrucache for CDNZ
License:    BSD
URL:        https://github.com/CDN-Z/lua-resty-lrucache

Source0:    https://github.com/CDN-Z/lua-resty-lrucache/archive/refs/tags/v%{version}.tar.gz#%{name}.tar.gz

BuildArch:      noarch
BuildRequires:  cdnz-luajit
Requires:       cdnz-luajit

%define lua_ver    5.1
%define _luapkgdir %{_datadir}/lua/%{lua_ver}
%define luajit_prefix /usr/local/cdnz/luajit2.1

# For Rocky Linux 9.3
%if 0%{?rhel} >= 9
%global debug_package %{nil}
%global _enable_debug_package 0
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}
%endif

%description
Lua module for LRU cache

%prep
%setup -q -n %{name}-%{version}

%build

%install
install -d %{buildroot}%{luajit_prefix}/resty/lrucache

install lib/resty/*.lua %{buildroot}%{luajit_prefix}/resty/
install lib/resty/lrucache/*.lua %{buildroot}%{luajit_prefix}/resty/lrucache/

%files
%doc README.markdown
%{luajit_prefix}/resty/*
%{luajit_prefix}/resty/lrucache/*