%define nginx_version   1.27.1
%define cdnz_version    1.0.0
%define user            nginx

Name:       cdnz
Version:    1.27.1
Release:    1%{?dist}
Summary:    CDNZ based on Nginx 1.27.1, with OpenSSL 3.5.0, LuaJIT 2.1, Openrsty

Group:      System Environment/Daemons

License:    BSD
URL:        https://nginx.org/

Source0:    https://nginx.org/download/nginx-%{version}.tar.gz

Source1:    https://github.com/CDN-Z/lua-nginx-module/archive/refs/tags/v%{cdnz_version}.tar.gz#/lua-nginx-module.tar.gz
Source2:    https://github.com/CDN-Z/ngx_devel_kit/archive/refs/tags/v%{cdnz_version}.tar.gz#/ngx_devel_kit.tar.gz

Source3:    cdnz.service
Source4:    cdnz.init

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
%define nginx_prefix        %{cdnz_prefix}/nginx
%define zlib_prefix         %{cdnz_prefix}/zlib
%define openssl_prefix      %{cdnz_prefix}/openssl3
%define pcre2_prefix        %{cdnz_prefix}/pcre2
%define luajit_prefix       %{cdnz_prefix}/luajit2.1

%define luajit_inc          %{luajit_prefix}/include/luajit-2.1
%define luajit_lib          %{luajit_prefix}/lib

# For Rocky Linux 9.3
%if 0%{?rhel} >= 9
%global debug_package %{nil}
%global _enable_debug_package 0
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}
%endif

%description
High-performance Nginx web server optimized for CDN usage with LuaJIT,
OpenSSL 3.5.0, and various performance enhancements

%prep
%setup -q -n nginx-%{nginx_version}
# %setup -q -T -D -a 1
# %setup -q -T -D -a 2

tar -xzf %{_sourcedir}/lua-nginx-module.tar.gz -C .
tar -xzf %{_sourcedir}/ngx_devel_kit.tar.gz -C .

%build
LUAJIT_INC=%{luajit_inc} LUAJIT_LIB=%{luajit_lib} \
./configure \
    --prefix=%{nginx_prefix} \
    --with-cc='ccache gcc -fdiagnostics-color=always' \
    --with-cc-opt="-DNGX_LUA_ABORT_AT_PANIC -I%{zlib_prefix}/include -I%{pcre2_prefix}/include -I%{openssl_prefix}/include" \
    --with-ld-opt="-L%{zlib_prefix}/lib -L%{pcre2_prefix}/lib -L%{openssl_prefix}/lib -Wl,-rpath,%{zlib_prefix}/lib:%{pcre2_prefix}/lib:%{openssl_prefix}/lib" \
    --user=nginx \
    --group=nginx \
    --with-http_ssl_module \
    --with-http_v2_module \
    --with-http_v3_module \
    --with-http_realip_module \
    --with-http_addition_module \
    --with-http_sub_module \
    --with-http_gunzip_module \
    --with-http_gzip_static_module \
    --with-http_auth_request_module \
    --with-http_secure_link_module \
    --with-http_slice_module \
    --with-http_stub_status_module \
    --with-stream \
    --with-stream_ssl_module \
    --with-stream_ssl_preread_module \
    --with-stream_realip_module \
    --with-http_dav_module \
    --with-http_flv_module \
    --with-http_mp4_module \
    --with-threads \
    --with-file-aio \
    --with-pcre-jit \
    --with-compat \
    --add-module=./lua-nginx-module-%{cdnz_version} \
    --add-module=./ngx_devel_kit-%{cdnz_version}

make %{?_smp_mflags}

%pre
getent group %{user} || groupadd -f -r %{user}
getent passwd %{user} || useradd -M -g %{user} -s /bin/nologin %{user}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

mkdir -p %{buildroot}/usr/bin

ln -sf %{cdnz_prefix}/bin/cdnz %{buildroot}/usr/bin/
ln -sf %{cdnz_prefix}/nginx/sbin/nginx %{buildroot}/usr/bin/%{name}

mkdir -p %{buildroot}/usr/lib/systemd/system/
cp %{_sourcedir}/cdnz.service %{buildroot}/usr/lib/systemd/system/cdnz.service

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%attr(755,root,root) /usr/lib/systemd/system/cdnz.service
/usr/bin/cdnz
/usr/bin/%{name}

%dir %{cdnz_prefix}
%dir %{cdnz_prefix}/nginx

%dir %{nginx_prefix}
%dir %{nginx_prefix}/html
%dir %{nginx_prefix}/logs
%dir %{nginx_prefix}/sbin
%{nginx_prefix}/html/*
%{nginx_prefix}/sbin/nginx

%dir %{nginx_prefix}/conf
%config(noreplace) %{nginx_prefix}/conf/fastcgi.conf
%config(noreplace) %{nginx_prefix}/conf/fastcgi_params
%config(noreplace) %{nginx_prefix}/conf/koi-utf
%config(noreplace) %{nginx_prefix}/conf/koi-win
%config(noreplace) %{nginx_prefix}/conf/mime.types
%config(noreplace) %{nginx_prefix}/conf/nginx.conf
%config(noreplace) %{nginx_prefix}/conf/scgi_params
%config(noreplace) %{nginx_prefix}/conf/uwsgi_params
%config(noreplace) %{nginx_prefix}/conf/win-utf
%config(noreplace) %{nginx_prefix}/conf/*.default

%preun

%postun
