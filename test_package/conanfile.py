from conans import ConanFile, CMake
import os


channel = os.getenv("CONAN_CHANNEL", "stable")
username = os.getenv("CONAN_USERNAME", "lasote")


class LeveldbTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "leveldb/1.19@%s/%s" % (username, channel)
    generators = "cmake"

    def build(self):
        cmake = CMake(self.settings)
        self.run('cmake "%s" %s' % (self.conanfile_directory, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def imports(self):
        self.copy("*.dll", "bin", "bin")
        self.copy("*.so", "lib", "bin")
        self.copy("*.dylib", "lib", "bin")

    def test(self):
        os.chdir("bin")
        self.run("LD_LIBRARY_PATH=$(pwd) && .%sexample" % os.sep)
