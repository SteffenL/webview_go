# MIT License
#
# Copyright (c) 2023 webview
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# This script checks the files of the libraries embedded within this project
# and ensures that the files match the remote files.
# See meta.txt for each library.

import argparse
from configparser import ConfigParser
from dataclasses import dataclass
import logging
import os
import sys
from tempfile import NamedTemporaryFile, TemporaryDirectory
from typing import Mapping, Optional, Sequence
from urllib.parse import urlparse
from urllib.request import urlopen, urlretrieve
from zipfile import ZipFile

def get_project_dir():
    return os.path.dirname(os.path.dirname(__file__))

def get_libs_dir():
    return os.path.join(get_project_dir(), "libs")

def get_lib_dir(lib_name: str):
    return os.path.join(get_libs_dir(), lib_name)

def check_local_file_against_remote_file(local_path: str, remote_path: str):
    logging.debug(f"Retrieving remote file: {remote_path}")
    with urlopen(remote_path) as remote_file:
        remote_content = remote_file.read()
    with open(local_path, "rb") as local_file:
        local_content = local_file.read()
    if remote_content != local_content:
        raise Exception(f"File mismatch: '{local_path}' doesn't match remote file '{remote_path}'")
    logging.debug(f"Local file '{local_path}' matches remote file '{remote_path}'")

def check_local_files_equivalent(first: str, second: str):
    with open(first, "rb") as first_file:
        first_content = first_file.read()
    with open(second, "rb") as second_file:
        second_content = second_file.read()
    if first_content != second_content:
        raise Exception(f"File mismatch: '{first}' doesn't match '{second}'")
    logging.debug(f"Local file '{first}' matches Local file '{second}'")


def make_lib_path(lib_name: str, sub_path: str):
    project_dir = get_project_dir()
    libs_root_dir = os.path.join(project_dir, "libs")
    abs_path = os.path.join(libs_root_dir, lib_name, sub_path)
    abs_path = os.path.realpath(abs_path)
    return abs_path

@dataclass
class LibMetaGithub:
    repository: str

    def __init__(self, config: Mapping[str, str]):
        self.repository = config["repository"]

@dataclass
class LibMetaNuget:
    package: str

    def __init__(self, config: Mapping[str, str]):
        self.package = config["package"]

@dataclass
class LibMeta:
    internal_name: str
    name: str
    version: str
    github: Optional[LibMetaGithub]
    nuget: Optional[LibMetaNuget]
    check: Mapping[str, str]

    def __init__(self, internal_name: str, config: Mapping[str, str]):
        self.internal_name = internal_name

        meta = config["meta"]
        self.name = meta["name"]
        self.version = meta["version"]

        try:
            self.github = LibMetaGithub(config["github"])
        except KeyError:
            self.github = None

        try:
            self.nuget = LibMetaNuget(config["nuget"])
        except KeyError:
            self.nuget = None

        try:
            self.check = config["check"]
        except KeyError:
            self.check = {}

def load_lib_meta(lib_name: str):
    lib_dir = get_lib_dir(lib_name)
    parser = ConfigParser()
    parser.optionxform = str
    parser.read(os.path.join(lib_dir, "meta.txt"))
    return LibMeta(lib_name, parser)

def load_all_libs_meta() -> Sequence[LibMeta]:
    lib_names = os.listdir(get_libs_dir())
    return [load_lib_meta(name) for name in lib_names]

def check_libs(libs: Sequence[LibMeta]):
    for lib in libs:
        logging.info(f"Library: {lib.name} ({lib.version})")
        if lib.github:
            logging.debug("Remote file location: GitHub")
            for k, v in lib.check.items():
                logging.info(f"  File: {k}")
                local_path = make_lib_path(lib.internal_name, k)
                remote_path = f"https://raw.githubusercontent.com/{lib.github.repository}/{lib.version}/{v}"
                check_local_file_against_remote_file(local_path, remote_path)
        elif lib.nuget:
            logging.debug("Remote file location: NuGet")
            remote_path = f"https://www.nuget.org/api/v2/package/{lib.nuget.package}/{lib.version}"
            with TemporaryDirectory() as temp_dir:
                with NamedTemporaryFile() as temp_zip_file:
                    logging.debug(f"Retrieving remote file: {remote_path}")
                    urlretrieve(remote_path, temp_zip_file.name)
                    zip = ZipFile(temp_zip_file.name)
                    for k, v in lib.check.items():
                        logging.info(f"  File: {k}")
                        zip.extract(v, temp_dir)
                        local_path = make_lib_path(lib.internal_name, k)
                        temp_path = os.path.join(temp_dir, v)
                        check_local_files_equivalent(local_path, temp_path)
        else:
            raise Exception("Need to know the remote location of the files to check")

def main(args):
    logging.getLogger().setLevel(("WARNING", "INFO", "DEBUG")[args.v])
    check_libs(load_all_libs_meta())

def parse_args(args: Sequence[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", help="Verbose output", action="count", default=0)
    return parser.parse_args(args)

if __name__ == "__main__":
    main(parse_args(sys.argv[1:]))
