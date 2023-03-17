#!/bin/sh

set -e

conan export cc
conan create libc -pr:h ./Linux-x86_64 --build=missing
conan create libc -pr:h ./Linux-x86 --build=missing
conan export-pkg sysroot/ -o os_target=Linux -o arch_target=x86_64
conan create cc -o os_target=Linux -o arch_target=x86_64
