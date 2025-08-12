import argparse
import os
import shutil
import subprocess
from enum import Enum

class Platform(Enum):
    X64 = "x64"
    WIN32 = "Win32"

class Configuration(Enum):
    Debug = "Debug"
    Release = "Release"

class Action(Enum):
    CLEAN = "clean"
    GENERATE = "generate"
    BUILD_DEBUG = "build_debug"
    BUILD_RELEASE= "build_release"
    CLANG_FORMAT = "clang_format"

class Config:
    BUILD_FOLDER = "build"
    CMAKE_GENERATOR = "Visual Studio 17 2022"
    PLATFORM = Platform.X64 #Platform.WIN32
    FRESH = True
    CLEAN = True
    VERBOSE = False
    SOURCE_DIR = "FightClub"

###############################################################

FRESH_ARG = "--fresh" if Config.FRESH else ""
CLEAN_ARG = "--clean-first" if Config.CLEAN else ""
VERBOSE_ARG = "--verbose" if Config.VERBOSE else ""


def remove_build_folder():
    if os.path.exists(Config.BUILD_FOLDER):
        shutil.rmtree(Config.BUILD_FOLDER)
        print(f"removed {Config.BUILD_FOLDER} folder.")
    else:
        print(f"{Config.BUILD_FOLDER} folder does not exist.")


def get_cmake_command(action):
    cmake_flags = {
        "generator" : f'-G "{Config.CMAKE_GENERATOR}"',
        "platform": f"-A {Config.PLATFORM.value}",
        "fresh": "--fresh" if Config.FRESH else "",
        "clean_first": "--clean-first" if Config.CLEAN else "",
        "verbose": "--verbose" if Config.VERBOSE else "",
        }

    if action == Action.Generate:
        return f'cmake .. {cmake_flags["generator"]} {cmake_flags["platform"]} {cmake_flags["fresh"]}'
    elif action in (Action.BUILD_DEBUG, Action.BUILD_RELEASE):
        configuration = (
            Configuration.Debug
            if action == Action.BUILD_DEBUG
            else Configuration.Release
            )
        return f'cmake --build . {cmake_flags["clean_first"]} {cmake_flags["verbose"]} --config {configuration.value}'
    return None


def run_command(command):
    result = subprocess.run(command, shell=True)
    return result.returncode == 0


def generate_project_files():
    if not os.path.exists(Config.BUILD_FOLDER):
        os.makedirs(Config.BUILD_FOLDER)
        print(f"Generated project files with comamnd: {command}")

    os.chdir(Config.BUILD_FOLDER)
    command = get_cmake_command(Action.GENERATE)
    print(f"Generated project files with command: {command}")

    if run_command(command):
        print("Project files generated succeddfully.")
    else:
        print("Failed to generate project files.")
    os.chdir("..")


def build_project(configuration=Configuration.Release):
    if not os.path.exists(Config.BUILD_FOLDER):
        print(f"{Config.Build_FOLDER} folder does not exist. Please generate project files first.")
        return
        
    os.chdir(Config.BUILD_FOLDER)
    command = get_cmake_command(
        Action.BUILD_DEBUG
        if configuration == Configuration.Debug
        else Action.BUILD_RELEASE
    )

    if run_command(command):
        print(f"Project built successfully in {configuration} mode.")
    else:
        print(f"Failed to build in {configuration} mode.")

    os.chdir("..")


def run_clang_format(source_dir):
     #find all .cpp and .h files in the specified source directory
    format_sources = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.cpp') or file.endswith('.h'):
                format_sources.append(os.path.join(root,file))

    if not format_sources:
        print(f'No source files found in {source_dir}.')
        return

    #run clang-format command
    command = ['clang-format', '-i'] + format_sources
    result = subprocess.run(command)
    if result.returncode == 0:
        print('Clang-format successfully applied.')
    else:
        print('Error running clang-format')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CMake Automation Script")
    parser.add_argument("action", type=Action, choices=list(Action), help="Action to perform")
    args = parser.parse_args()

    action_map = {
        Action.CLEAN: remove_build_folder,
        Action.GENERATE: generate_project_files,
        Action.BUILD_DEBUG: lambda: build_project(Configuration.Debug),
        Action.BUILD_RELEASE: lambda: build_project(Configuration.Release),
        Action.CLANG_FORMAT: lambda: run_clang_format(Config.SOURCE_DIR),
    }

    selected_action = args.action

    if selected_action in action_map:
        action_map[selected_action]()
    else:
        print(f"Action '{selected_action}' is not implemented.")
