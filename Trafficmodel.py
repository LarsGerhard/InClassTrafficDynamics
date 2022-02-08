# Imports
from numpy import array, linspace, sqrt, pi, concatenate
from numpy.random import choice
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
r = 1000 # Radius of the roundabout
ncars = 50 # Number of cars in our system

# Initial Conditions
x0 = linspace(0, 2 * pi * r, ncars)
v0 = choice(28, ncars)
V1 = concatenate([x0, v0])

# set the time interval for solving (in mks)
t0 = 0
tf = 15 * 60

# Form Time array
tspace = linspace(t0, tf, int(4. * tf / 10.))  # Uses given ratio of steps -> time to generate number of steps needed


def main():
    X = odeint(ratefunc, V1, tspace, tfirst=True)

    # unpack the results. In the output array, variables are columns, times are rows
    xout = X[:ncar]
    vout = X[ncar:]

    # For plotting
    plot(xout, vout)




# Differential Equation
def ratefunc(t, V):
    # RATE_FUNC: IDM Car model
    # Model a car approaching a solid wall

    # unpack
    x = V[:ncars]  # position
    v = V[ncars:]  # velocity
    deltav = v - vblock

    # Compute acceleration from IDM

    s = (Xblock - L) - x

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
