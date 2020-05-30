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

import unittest
from unittest.mock import patch, call
import trackpack


class TestTrackPack(unittest.TestCase):

    @patch("os.walk")
    def test_find_audiofiles_returns_audio_files(self, walk_mock):
        walk_mock.return_value = iter([
            ('projdir', [], ['proj stem2.wav', 'proj stem4.wav',
                             'proj stem1.wav', 'proj.wav', 'proj stem3.wav']),
        ])
        (master, stems) = trackpack.find_audiofiles("proj", "/tmp/export")
        walk_mock.assert_called_with('/tmp/export')
        self.assertEqual('proj.wav', master)
        self.assertListEqual(['proj stem2.wav', 'proj stem4.wav',
                              'proj stem1.wav', 'proj stem3.wav'], stems)

    @patch("os.walk")
    def test_find_audiofiles_returns_only_related_audio_files(self, walk_mock):
        walk_mock.return_value = iter([
            ('projdir', [], ['proj stem2.wav', 'ignore.txt', 'proj stem1.wav',
                             'proj.wav', 'archive.zip', "proj unrelated.mp3"]),
        ])
        (_, stems) = trackpack.find_audiofiles("proj", "/tmp/export")
        self.assertListEqual(['proj stem2.wav', 'proj stem1.wav'], stems)

    @patch("os.walk")
    def test_find_audiofiles_master_track_matches_project_name(self, walk_mock):
        walk_mock.return_value = iter([
            ('projdir', [], ['example.wav', 'proj stem4.wav',
                             'proj stem1.wav', 'proj.wav', 'proj stem3.wav']),
        ])
        (master, _) = trackpack.find_audiofiles("example", "/tmp/export")
        self.assertEqual('example.wav', master)

    @patch("os.walk")
    def test_find_audiofiles_fails_if_no_master(self, walk_mock):
        walk_mock.return_value = iter([
            ('projdir', [], ['proj stem1.wav', 'proj stem2.wav']),
        ])

        with self.assertRaises(trackpack.MissingFileException):
            trackpack.find_audiofiles("proj", "/tmp/export")

    @patch("os.walk")
    def test_find_audiofiles_fails_if_no_stems(self, walk_mock):
        walk_mock.return_value = iter([
            ('projdir', [], ['proj.wav']),
        ])

        with self.assertRaises(trackpack.MissingFileException):
            trackpack.find_audiofiles("proj", "/tmp/export")

    @patch("trackpack.ZipFile", autospec=True)
    def test_pack_files_creates_archive_of_stems(self, zip_mock):
        trackpack.pack_files("/tmp/projdir", "projname", ["a.wav", "b.wav", "c.wav"])
        zip_mock.assert_has_calls([call("/tmp/projdir/projname.zip", "w"),
                                   call().__enter__(),
                                   call().__enter__().write("a.wav"),
                                   call().__enter__().write("b.wav"),
                                   call().__enter__().write("c.wav"),
                                   call().__exit__(None, None, None)])
