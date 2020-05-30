# trackpack - Package audio tracks
#
# Copyright (C) 2020  offa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from zipfile import ZipFile

class MissingFileException(Exception):
    pass


def find_audiofiles(project_name, project_path):
    (_, _, filenames) = next(os.walk(project_path))
    master = "{}.wav".format(project_name)
    filenames = list(filter(lambda f: f.endswith(".wav"), filenames))

    if master not in filenames:
        raise MissingFileException("Master track not found")
    filenames.remove(master)

    if not filenames:
        raise MissingFileException("No stems found")

    return (master, filenames)


def pack_files(project_dir, project_name, files):
    with ZipFile("{}.zip".format(os.path.join(project_dir, project_name)), "w") as archive:
        for file in files:
            archive.write(file)


if __name__ == '__main__':
    pass
