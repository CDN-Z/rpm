Name:           lua51
Version:        5.1.5
Release:        1%{?dist}
Summary:        Lua 5.1.5 programming language

License:        MIT
URL:            http://www.lua.org/
Source0:        http://www.lua.org/ftp/lua-%{version}.tar.gz

BuildRequires:  gcc make readline-devel
Requires:       readline

%define lua_prefix /usr/local/lua5.1

%description
Lua is a powerful, light-weight programming language designed for extending
applications. This package provides Lua 5.1.5, installed in a separate prefix
to avoid conflicts with system Lua versions.

%prep
%setup -q -n lua-%{version}

%build
make linux CFLAGS="%{optflags} -DLUA_USE_LINUX" \
     MYLIBS="-lreadline" \
     LDFLAGS="%{__global_ldflags}"

%install
make install INSTALL_TOP=%{buildroot}%{lua_prefix} \
     INSTALL_LIB=%{buildroot}%{lua_prefix}/lib \
     INSTALL_CMOD=%{buildroot}%{lua_prefix}/lib/lua/5.1 \
     INSTALL_LMOD=%{buildroot}%{lua_prefix}/share/lua/5.1

# Install pkg-config file
mkdir -p %{buildroot}%{lua_prefix}/lib/pkgconfig
cat > %{buildroot}%{lua_prefix}/lib/pkgconfig/lua.pc << EOF
prefix=%{lua_prefix}
exec_prefix=\${prefix}
libdir=\${prefix}/lib
includedir=\${prefix}/include

Name: Lua
Description: Lua 5.1.5 programming language
Version: %{version}
Libs: -L\${libdir} -llua -lm
Cflags: -I\${includedir}
EOF

%files
%{lua_prefix}/bin/*
%{lua_prefix}/lib/liblua.a
%{lua_prefix}/lib/liblua.so
%{lua_prefix}/lib/liblua.so.5.1
%{lua_prefix}/lib/liblua.so.5.1.5
%{lua_prefix}/include/*
%{lua_prefix}/lib/pkgconfig/lua.pc
%{lua_prefix}/share/lua/5.1/*
%doc README