# Imports
from numpy import array, linspace, sqrt
from matplotlib.pyplot import figure, subplot, show
from scipy.integrate import odeint

# Initial Variables (In mks units)
a = 0.7  # Acceleration
b = 2.  # Deceleration
delta = 4.  # Acceleration exponent
L = 5.  # Vehicle length
xmin = 2.  # Minimum gap
T = 1.8  # Time headway
vdes = 28  # Desired speed
Xblock = 5000  # Barrier position
vblock = 0  # Velocity of the block

# Initial Conditions
x0 = 0
v0 = 0
V1 = array([x0, v0])

# set the time interval for solving
t0 = 0
tf = 300

# Form Time array
tspace = linspace(t0, tf, 400)  # 400 steps for nice plot


def main():
    X = odeint(singleratefunc, V1, tspace, tfirst=True)

    # unpack the results. In the output array, variables are columns, times are rows
    xout = X[:, 0]
    vout = X[:, 1]

    # For plotting
    plot(xout, vout)


# Differential Equation
def singleratefunc(t, V):
    # RATE_FUNC: IDM Car model
    # Model a car approaching a solid wall

    # unpack
    x = V[0]  # position
    v = V[1]  # velocity
    s = (Xblock - L) - x
    deltav = v - vblock

    # Compute acceleration from IDM

    a_idm = a * ((1 - (v / vdes) ** delta) - (followdist(v, deltav) / s) ** 2)

    # compute derivatives
    dx = v
    dv = a_idm

    # pack rate array
    rate = array([dx, dv])
    return rate


def followdist(v, deltav):
    sstar = xmin + v * T + (v * deltav) / (2 * sqrt(a * b))
    return sstar


# Function used to plot everything
def plot(x1, x2):
    fig = figure()

    ax1 = subplot()
    ax1.plot(tspace, x1, 'b')
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('distance (m)', color='b')
    ax1.tick_params('y', colors='b')

    ax2 = ax1.twinx()
    ax2.plot(tspace, x2, 'r')
    ax2.set_ylabel('velocity (m/s)', color='r')
    ax2.tick_params('y', colors='r')

    fig.tight_layout()

    show()


main()
