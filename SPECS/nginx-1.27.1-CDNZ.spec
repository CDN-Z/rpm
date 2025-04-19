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

%define         nginx_version 3.0.12


Source0:        nginx-%{nginx_version}.tar.gz
