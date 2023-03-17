
import os
from typing import Any

from conan import ConanFile
from conan.tools.gnu.get_gnu_triplet import _get_gnu_triplet

class LibcConan(ConanFile):
    name = "libc"
    version = "1.0"
    license = "GPL-2.0"
    url = "https://www.gnu.org/software/libc/"
    description = "GNU C library"

    settings: Any = ["os", "arch", "compiler", "build_type"]
    package_type = "shared-library"

    def build_requirements(self):
        self.tool_requires("cc/1.0", options={"libc": False})

    def build(self):
        pass

    def package(self):
        include = os.path.join(self.package_folder, "include", self._triplet)
        os.makedirs(include, exist_ok=True)
        with open(os.path.join(include, "stdio.h"), "w") as f:
            f.write("#error this is a fake header ")
            
    @property
    def _triplet(self):
        return _get_gnu_triplet(str(self.settings.os), str(self.settings.arch), 'gcc')
        

