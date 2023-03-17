
from typing import Any
import shutil
import os

from conan import ConanFile

class CCConan(ConanFile):

    name = "cc"
    version = "1.0"
    license = "GPL"
    url = "https://www.gnu.org/software/gcc/"
    description = "GCC, the GNU Compiler Collection"

    settings: Any = ("os", "arch", "compiler", "build_type")
    options: Any = {
        "libc": [True, False],
        "os_target": ["Linux"],
        "arch_target": ["x86", "x86_64"],
    }
    package_type = "application"
    default_options = {"libc": True}

    def configure(self):
        # record target information in options
        if settings_target := getattr(self, "settings_target", None):
            self.options.os_target = self.options.os_target or settings_target.os
            self.options.arch_target = self.options.arch_target or settings_target.arch

    def requirements(self):
        if self.options.libc:
            self.build_requires("sysroot/1.0", options={
                'os_target': self.options.os_target,
                'arch_target': self.options.arch_target})

    def package_id(self):
        if self.info.options.arch_target == "x86" and self.info.options.os_target == "Linux":
            self.info.options.arch_target = "x86_64" # multiarch covers both

    def build(self):
        if self.options.libc:
            sysroot = self.dependencies.get("sysroot", build=True).package_folder
            self.output.highlight(f"would call ./configure ... --with-sysroot=${{prefix}}/sysroot --with-build-sysroot={sysroot}")

    def package(self):
        if self.options.libc:
            shutil.copytree(
                self.dependencies.get("sysroot", build=True).package_folder,
                os.path.join(self.package_folder, "sysroot"))


