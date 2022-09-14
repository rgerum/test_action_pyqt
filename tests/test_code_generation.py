import unittest
import numpy as np

import sys
import os
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib import _pylab_helpers
import pylustrator
from qtpy import QtWidgets

class TestFits(unittest.TestCase):

    def setUp(self):
        print("setup")
        self.filename = Path(self.id().split(".")[-1] + ".py")
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
        tmp_file = Path(str(self.filename) + ".tmp")
        if tmp_file.exists():
            tmp_file.unlink()

    def test_fitCamParametersFromObjects(self):
        app = QtWidgets.QApplication(sys.argv)

    def test_fitCamParametersFromObjects2(self):
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



