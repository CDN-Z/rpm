# CDNZ Package Builder

This repository contains everything needed to build optimized packages for CDNZ, a high-performance Nginx-based CDN solution with LuaJIT, OpenSSL 3.5.0, and various performance enhancements.

## Requirements

- Rocky Linux 9.x or compatible RHEL-based system
- Root or sudo access
- Internet connection to download source packages

## Quick Start

1. Install required dependencies:
   ```bash
   ./init.sh
   ```


## Package Components

- **cdnz-zlib**: Optimized zlib 1.2.12
- **cdnz-openssl3**: Enhanced OpenSSL 3.5.0 with KTLS support
- **cdnz-pcre2**: PCRE2 10.44 with JIT support
- **cdnz-luajit**: LuaJIT 2.1 optimization
- **cdnz-lua-resty-core**: Lua modules for Nginx
- **cdnz-resty-lrucache**: Lua LRU cache
- **cdnz**: The main Nginx-based CDN package

## Directory Structure

- `specs/`: RPM spec files for all packages
- `sources/`: Downloaded source archives
- `build/`: Build artifacts and compiled RPMs
- `packages/`: Final RPM packages and YUM repository

## Customization

Edit the Makefile to change package versions or build options. Each package has a corresponding spec file in the `specs/` directory that can be modified to customize build options.

## Special Features

1. KTLS support in OpenSSL for kernel TLS offloading
2. HTTP/3 and QUIC protocol support
3. LuaJIT integration for programmable CDN features
4. Optimized for high-throughput, low-latency content delivery

## License

This project is distributed under the BSD license.

## Support

For support, please contact admin@cdn-z.com or create an issue on this repository.