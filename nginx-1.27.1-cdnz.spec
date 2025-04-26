Name:       cdnz
Version:    1.27.1
Release:    1%{?dist}
Summary:    CDNZ based on Nginx 1.27.1, with OpenSSL 3.5.0, LuaJIT 2.1, Openrsty

Group:      System Environment/Daemons

License:    BSD
URL:        https://nginx.org/

Source0:    https://nginx.org/download/nginx-%{version}.tar.gz
Source1:    https://github.com/CDN-Z/lua-resty-core/archive/refs/tags/lua-resty-core.tar.gz
Source2:    https://github.com/CDN-Z/lua-nginx-module/archive/refs/tags/lua-nginx-module.tar.gz
Source3:    https://github.com/CDN-Z/lua-resty-lrucache/archive/refs/tags/lua-resty-lrucache.tar.gz

Source4:    cdnz.service
Source5:    cdnz.init

BuildRequires:      cmake, make, gcc, perl
BuildRequires:      cdnz-zlib-devel >= 1.2.11
BuildRequires:      cdnz-zlib >= 1.2.11
BuildRequires:      cdnz-openssl3-devel >= 3.5.0
BuildRequires:      cdnz-openssl3 >= 3.5.0
BuildRequires:      cdnz-pcre2-devel >= 10.44
BuildRequires:      cdnz-pcre2 >= 10.44
BuildRequires:      cdnz-luajit >= 2.1
BuildRequires:      systemd

Requires:           systemd

%define cdnz_prefix         %{_usr}/local/%{name}
%define zlib_prefix         %{cdnz_prefix}/zlib
%define openssl_prefix      %{cdnz_prefix}/openssl3
%define pcre2_prefix        %{cdnz_prefix}/pcre2
%define luajit_prefix       %{cdnz_prefix}/luajit2.1
%define lua_package_path    %{cdnz_prefix}/lib/lua

# For Rocky Linux 9.3
%if 0%{?rhel} >= 9
%global debug_package %{nil}
%global _enable_debug_package 0
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}
%endif

%prep
%setup -q


