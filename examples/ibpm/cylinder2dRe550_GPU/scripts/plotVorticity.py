"""
Computes, plots, and saves the 2D vorticity field from a PetIBM simulation
after 1200 time steps (3 non-dimensional time-units).
"""

import pathlib
import h5py
import numpy
from matplotlib import pyplot


simu_dir = pathlib.Path(__file__).absolute().parents[1]
data_dir = simu_dir / 'output'

# Read vorticity field and its grid from files.
name = 'wz'
filepath = data_dir / 'grid.h5'
f = h5py.File(filepath, 'r')
x, y = f[name]['x'][:], f[name]['y'][:]
X, Y = numpy.meshgrid(x, y)
timestep = 1200
filepath = data_dir / '{:0>7}.h5'.format(timestep)
f = h5py.File(filepath, 'r')
wz = f[name][:]

# Read body coordinates from file.
filepath = simu_dir / 'circle.body'
with open(filepath, 'r') as infile:
    xb, yb = numpy.loadtxt(infile, dtype=numpy.float64,
                           unpack=True, skiprows=1)

pyplot.rc('font', family='serif', size=16)

# Plot the filled contour of the vorticity.
fig, ax = pyplot.subplots(figsize=(6.0, 6.0))
ax.grid()
ax.set_xlabel('x')
ax.set_ylabel('y')
levels = numpy.linspace(-32.0, 32.0, 32)
ax.contour(X, Y, wz, levels=levels, colors='black')
ax.plot(xb, yb, color='red')
ax.set_xlim(-0.6, 1.6)
ax.set_ylim(-0.8, 0.8)
ax.set_aspect('equal')
fig.tight_layout()

pyplot.show()

# Save figure.
fig_dir = simu_dir / 'figures'
fig_dir.mkdir(parents=True, exist_ok=True)
filepath = fig_dir / 'wz{:0>7}.png'.format(timestep)
fig.savefig(str(filepath), dpi=300)
