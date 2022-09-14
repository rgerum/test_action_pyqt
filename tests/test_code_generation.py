#!/usr/bin/env python
# -*- coding: utf-8 -*-
# test_code_generation.py

# Copyright (c) 2016-2020, Richard Gerum
#
# This file is part of Pylustrator.
#
# Pylustrator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pylustrator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pylustrator. If not, see <http://www.gnu.org/licenses/>
import sys
sys.argv = ["-platform", "minimal"]
print("start")
print(sys.argv)
import unittest
print("import qt")
print("done")


print("start test")

class TestFits(unittest.TestCase):

    def test_fitCamParametersFromObjects(self):
        print("read file")


if __name__ == '__main__':
    unittest.main()


