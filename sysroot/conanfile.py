import os
from typing import Any
import shutil

from conan import ConanFile
from conan.api.conan_api import ConanAPI
from conan.api.model import ListPattern, RecipeReference, PackagesList, PkgReference


class BasicConanfile(ConanFile):
    name : str = "sysroot"
    version :str = "1.0"
    description : str = "system libraries for a cross compiler"
    license = "TBD"
    homepage = "TBD"

    options : Any = {
        "os_target": ["Linux"],
        "arch_target": ["x86", "x86_64"],
    }
    settings : Any = []

    build_policy = "never" 

    def package(self):

        def timestamp(pair):
            rev, value = pair
            return value['timestamp']

        # FIXME this is illegal but we're doing it anyway
        api = ConanAPI()
        packages : PackagesList = api.list.select(ListPattern("libc/1.0:*"))
        rrevs = list(sorted(packages.serialize()['libc/1.0']['revisions'].items(), key=timestamp))                        
        rev, latest = rrevs.pop()

        def copy_libc(arch):
            for pkgId, pkg in latest['packages'].items():
                settings = pkg['info']['settings']
                if settings['arch'] != arch or settings['os'] != str(self.options.os_target):
                    continue
                ref = RecipeReference(name='libc', version="1.0", revision=rev)
                pkgRef = PkgReference(ref=ref, package_id=pkgId)
                path = api.cache.package_path(pkgRef)
                self.output.highlight(f"copying files for {self.options.os_target}-{arch} from {path}")
                shutil.copytree(path, self.package_folder, dirs_exist_ok=True)
                
        copy_libc(str(self.options.arch_target))
        if self.options.arch_target == "x86_64" and self.options.os_target == "Linux":
            copy_libc("x86") # copy 32 bit libc too for multiarch

