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
import matplotlib
matplotlib.use('agg')
import unittest
import numpy as np
import sys
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib import _pylab_helpers
print("import qt")
from qtpy import QtCore, QtWidgets, QtGui
print("done")

""" some magic to prevent PyQt5 from swallowing exceptions """
# Back up the reference to the exceptionhook
sys._excepthook = sys.excepthook
# Set the exception hook to our wrapping function
sys.excepthook = lambda *args: sys._excepthook(*args)

print("start test")


class TestFits(unittest.TestCase):

    def setUp(self):
        print("setup")
        self.filename = Path(self.id().split(".")[-1]+".py")
        with self.filename.open("w") as fp:
            print("write tmp file")
            fp.write("""
import matplotlib.pyplot as plt
import numpy as np

# now import pylustrator
import pylustrator

# activate pylustrator
pylustrator.start()

# build plots as you normally would
np.random.seed(1)
t = np.arange(0.0, 2, 0.001)
y = 2 * np.sin(np.pi * t)
a, b = np.random.normal(loc=(5., 3.), scale=(2., 4.), size=(100,2)).T
b += a

plt.figure(1)
plt.subplot(131)
plt.plot(t, y)

plt.subplot(132)
plt.plot(a, b, "o")

plt.subplot(133)
plt.bar(0, np.mean(a))
plt.bar(1, np.mean(b))

# show the plot in a pylustrator window
plt.show(hide_window=True)
""")

    def tearDown(self):
        self.filename.unlink()
        tmp_file = Path(str(self.filename)+".tmp")
        if tmp_file.exists():
            tmp_file.unlink()

    def test_fitCamParametersFromObjects(self):
        print("read file")
        with open(self.filename, "rb") as fp:
            text = fp.read()
        print("exec file")
        exec(compile(text, self.filename, 'exec'), globals())

        print("get figure")
        for figure in _pylab_helpers.Gcf.figs:
            figure = _pylab_helpers.Gcf.figs[figure].canvas.figure
            print("select element")
            figure.figure_dragger.select_element(figure.axes[0])

            print("start move")
            figure.selection.start_move()
            figure.selection.addOffset((-1, 0), figure.selection.dir)
            print("end move")
            figure.selection.end_move()
            print("save")
            figure.change_tracker.save()

        print("open saved file")
        with self.filename.open("r") as fp:
            in_block = False
            found = False
            block = ""
            for line in fp:
                if in_block is True:
                    block += line
                    if line.startswith("plt.figure(1).axes[0].set_position([0.123333, 0.110000, 0.227941, 0.770000])"):
                        found = True
                if line.startswith("#% start: automatic generated code from pylustrator"):
                    in_block = True
                if line.startswith("#% end: automatic generated code from pylustrator"):
                    in_block = False

        self.assertTrue(found, "Figure movement not correctly written to file")


if __name__ == '__main__':
    unittest.main()


