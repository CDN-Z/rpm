Name:       cdnz-ccache
Version:    4.11.2
Release:    1%{?dist}
Summary:    Fast compiler cache for CDNZ
License:    BSD
URL:        https://ccache.dev/
Source0:    https://github.com/ccache/ccache/releases/download/v%{version}/ccache-%{version}-linux-x86_64.tar.xz

# For Rocky Linux 9.3
%global debug_package %{nil}
%global _enable_debug_package 0
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

%define ccache_prefix /usr/local/cdnz/ccache

%description
ccache is a compiler cache.  It speeds up recompilation of C/C++ code
by caching previous compiles and detecting when the same compile is
being done again.  The main focus is to handle the GNU C/C++ compiler
(GCC), but it may also work with compilers that mimic GCC good enough.

%prep
%setup -q -n ccache-%{version}-linux-x86_64

%install
# Create directories
mkdir -p %{buildroot}%{ccache_prefix}/bin
mkdir -p %{buildroot}%{ccache_prefix}/libexec
mkdir -p %{buildroot}/etc/profile.d
mkdir -p %{buildroot}%{_sysconfdir}/ccache
mkdir -p %{buildroot}%{_bindir}

# Install binary
install -m 755 ccache %{buildroot}%{ccache_prefix}/bin/ccache
ln -sf %{ccache_prefix}/bin/ccache %{buildroot}%{_bindir}/ccache

# Create compiler symlinks
cd %{buildroot}%{ccache_prefix}/libexec
for comp in gcc g++ cc c++ clang clang++; do
    ln -sf ../bin/ccache ${comp}
done
cd -

# Create config file
cat > %{buildroot}%{_sysconfdir}/ccache/ccache.conf << EOF
max_size = 5G
umask = 002
hash_dir = false
compression = true
compression_level = 1
temporary_dir = /tmp/ccache
sloppiness = include_file_ctime,include_file_mtime,time_macros
EOF

# Create profile script
cat > %{buildroot}/etc/profile.d/ccache.sh << EOF
# Enable ccache for all users
export PATH=%{ccache_prefix}/libexec:\$PATH
export CCACHE_CONFIGPATH=%{_sysconfdir}/ccache/ccache.conf
EOF

%post
# Create ccache directory with proper permissions
mkdir -p /var/cache/ccache
chmod 1777 /var/cache/ccache
ldconfig

%files
%{ccache_prefix}
%{_bindir}/ccache
%config(noreplace) %{_sysconfdir}/ccache/ccache.conf
/etc/profile.d/ccache.sh