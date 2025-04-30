Name:       lua-resty-core
Version:    1.0.0
Release:    1%{?dist}
Summary:    Install lua-resty-core for CDNZ
License:    BSD
URL:        https://github.com/CDN-Z/lua-resty-core

Source0:    https://github.com/CDN-Z/lua-resty-core/archive/refs/tags/v%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  cdnz-luajit
Requires:       cdnz-luajit

%define lua_ver    5.1
%define _luapkgdir %{_datadir}/lua/%{lua_ver}

# For Rocky Linux 9.3
%if 0%{?rhel} >= 9
%global debug_package %{nil}
%global _enable_debug_package 0
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}
%endif

%description
New FFI-based Lua API for ngx_http_lua_module and/or
ngx_stream_lua_module

%prep
%setup -q -n %{name}-%{version}

%build

%install
install -d %{buildroot}%{_luapkgdir}/resty/core
install -d -p %{buildroot}%{_luapkgdir}/ngx/ssl
install lib/resty/*.lua %{buildroot}%{_luapkgdir}/resty/
install lib/resty/core/*.lua %{buildroot}%{_luapkgdir}/resty/core/
install lib/ngx/*.lua %{buildroot}%{_luapkgdir}/ngx/
install lib/ngx/ssl/*.lua %{buildroot}%{_luapkgdir}/ngx/ssl/

%files
%doc README.markdown
%{_luapkgdir}/resty/*
%{_luapkgdir}/ngx/*