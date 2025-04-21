Name:           nginx-cdnz
Version:        %{nginx_version}
Release:        1%{?dist}
Summary:        Nginx optimized for CDN VOD delivery
License:        BSD
URL:            https://nginx.org/

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  pcre-devel
BuildRequires:  zlib-devel
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
BuildRequires:  gd-devel
BuildRequires:  perl-devel
BuildRequires:  pam-devel
BuildRequires:  gperftools-devel
BuildRequires:  git
BuildRequires:  wget
BuildRequires:  cmake

Requires:       pcre
Requires:       openssl
Requires:       zlib
Provides:       webserver
Conflicts:      nginx

%define         nginx_version 1.27.1.2

Source0:        https://openresty.org/download/openresty-%{version}.tar.gz
Source1:        nginx.service
Source2:        nginx.logrotate
Source3:        nginx.conf

# Open-Resty Core
Source100:      https://github.com/CDN-Z/lua-resty-core/archive/refs/tags/lua-resty-core.tar.gz
Source101:      https://github.com/CDN-Z/lua-resty-lrucache/archive/refs/tags/lua-resty-lrucache.tar.gz
Source102:      https://github.com/CDN-Z/lua-nginx-module/archive/refs/tags/lua-nginx-module.tar.gz

# Logging
