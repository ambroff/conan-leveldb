from conans import ConanFile, CMake, tools, ConfigureEnvironment
import os


class LeveldbConan(ConanFile):
    name = "leveldb"
    version = "1.19"
    license = "https://github.com/google/leveldb/blob/master/LICENSE"
    url = "https://github.com/lasote/conan-leveldb"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    requires = "gperftools/2.5@lasote/stable"
    
    @property
    def zipped_folder(self):
        return "leveldb-%s" % self.version
    
    def source(self):
       tools.download("https://github.com/google/leveldb/archive/v%s.zip" % self.version, "leveldb.zip")
       tools.unzip("leveldb.zip")

    def build(self):
        if self.settings.os == "Linux" or self.settings.os == "Macos":
            env = ConfigureEnvironment(self.deps_cpp_info, self.settings)
            env_line = env.command_line_env.replace('CFLAGS="', 'CFLAGS="-fPIC ')
            self.run("chmod +x %s/build_detect_platform" % self.zipped_folder)                        
#             if self.settings.os == "Macos":
#                 old_str = '-install_name $libdir/$SHAREDLIBM'
#                 new_str = '-install_name $SHAREDLIBM'
#                 replace_in_file("./%s/configure" % self.ZIP_FOLDER_NAME, old_str, new_str)
#                      
            self.run("cd %s && %s make" % (self.zipped_folder, env_line))

    def package(self):
        self.copy("*", dst="include", src="%s/include" % self.zipped_folder, keep_path=True)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("LICENSE", src=self.zipped_folder, dst="", keep_path=False)
           
        if self.options.shared:
            self.copy("*.dll", dst="bin", keep_path=False)
            self.copy("*.so*", dst="lib", keep_path=False)
        else:
            self.copy("*.a", dst="lib", keep_path=False)


    def package_info(self):
        self.cpp_info.libs = ["leveldb"]
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
