from conans import ConanFile
import os

class LuaLpegConan(ConanFile):
    name = "lua-lpeg"
    license = "MIT"
    description = "lua Lpeg."
    url = "https://github.com/LuaDist/lpeg"

    # Settings and options
    settings = "os", "compiler", "arch"

    # Additional files to export
    exports_sources = ["premake5.lua"]

    # Iceshard conan tools
    python_requires = "conan-iceshard-tools/0.6.2@iceshard/stable"
    python_requires_extend = "conan-iceshard-tools.IceTools"

    # Dependencies
    requires = "lua/5.1.5@iceshard/stable"


    # Initialize the package
    def init(self):
        self.ice_init("premake5")
        self.build_requires = self._ice.build_requires

    # Build both the debug and release builds
    def ice_build(self):
        self.ice_generate()

        if self.settings.compiler == "Visual Studio":
            self.ice_build_msbuild("LuaLPeg.sln", ["Debug", "Release"])

        else:
            self.ice_build_make(["Debug", "Release"])

    def package(self):
        self.copy("LICENSE", src=self._ice.out_dir, dst="LICENSE")

        # Header files
        self.copy("*.h", "include", "{}".format(self._ice.out_dir), keep_path=False)

        # binaries
        build_dir = os.path.join(self._ice.out_dir, "bin")
        if self.settings.os == "Windows":
            self.copy("*.lib", "lib", build_dir, keep_path=True)
            self.copy("*.dll", "bin", build_dir, keep_path=True)
            self.copy("*.pdb", "bin", build_dir, keep_path=True)
        if self.settings.os == "Linux":
            self.copy("*.a", "lib", build_dir, keep_path=True)
            self.copy("*.so", "lib", build_dir, keep_path=True)

    def package_info(self):
        self.cpp_info.libdirs = []
        self.cpp_info.debug.libdirs = [ "lib/Debug" ]
        self.cpp_info.release.libdirs = [ "lib/Release" ]
        self.cpp_info.includedirs = [ "include" ]
        self.cpp_info.libs = [ "lpeg" ]

        # Enviroment info
        if self.settings.os == "Windows":
            self.env_info.LUA_CPATH.append(os.path.join(self.package_folder, "bin/Release/?.dll"))
        if self.settings.os == "Linux":
            self.env_info.LUA_CPATH.append(os.path.join(self.package_folder, "bin/Release/?.so"))
