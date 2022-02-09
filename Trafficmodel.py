# Imports
from numpy import linspace, sqrt, pi, concatenate, zeros
from numpy.random import choice
from matplotlib.pyplot import figure, subplot, show
from scipy.integrate import odeint

# Initial Variables (In mks units)
a = 0.1  # Acceleration
b = 2.  # Deceleration
delta = 4.  # Acceleration exponent
L = 5.  # Vehicle length
xmin = 2.  # Minimum gap
T = 1.8  # Time headway
vdes = 28  # Desired speed
r = 1000  # Radius of the roundabout
C = 2 * pi * r  # Circumference of the roundabout
ncars = 50  # Number of cars in our system

# Initial Conditions
x0 = linspace(0, C - 50, ncars)
v0 = choice(28, ncars)  # choice(28, ncars)
V1 = concatenate((x0, v0))

# set the time interval for solving (in mks)
t0 = 0
tf = 15 * 60

# Form Time array
tspace = linspace(t0, tf, int(4. * tf / 10.))  # Uses given ratio of steps -> time to generate number of steps needed


def main():
    M = odeint(ratefunc, V1, tspace, tfirst=True)
    # unpack the results. In the output array, variables are columns, times are rows
    xout = M[:, :ncars]
    vout = M[:, ncars:]
    # For plotting
    plot(xout, vout, tspace)


# Differential Equation
def ratefunc(t, V):
    # RATE_FUNC: IDM Car model
    # Model a car approaching a solid wall

    # unpack
    x = V[:ncars]  # position
    v = V[ncars:]  # velocity
    dv = zeros(ncars)

    # Compute acceleration from IDM

    for i in range(ncars):
        if (i + 1) == ncars:
            s = (x[0] - L) - (x[i] - C)
            deltav = (v[i] - v[0])

        else:
            s = ((x[i + 1] - L) - x[i])
            deltav = (v[i] - v[i + 1])

        # compute derivatives
        dv[i] = a * ((1 - (v[i] / vdes) ** delta) - (followdist(v[i], deltav) / s) ** 2)

    dx = v

    # pack rate array
    rate = concatenate((dx, dv))
    return rate


def followdist(v, deltav):
    sstar = xmin + v * T + (v * deltav) / (2 * sqrt(a * b))
    return sstar


# Function used to plot everything
def plot(x1, x2, t):
    fig = figure()

    ax1 = subplot()
    ax1.plot(t, x1[:, 10], 'b')
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('distance (m)', color='b')
    ax1.tick_params('y', colors='b')

    ax2 = ax1.twinx()
    ax2.plot(t, x2[:, 10], 'r')
    ax2.set_ylabel('velocity (m/s)', color='r')
    ax2.tick_params('y', colors='r')

    fig.tight_layout()

    show()

    fig = figure()

    ax1 = subplot()
    ax1.plot(t, x1, 'b')
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('distance (m)', color='b')
    ax1.tick_params('y', colors='b')

    ax2 = ax1.twinx()
    ax2.plot(t, x2, 'r')
    ax2.set_ylabel('velocity (m/s)', color='r')
    ax2.tick_params('y', colors='r')

    fig.tight_layout()
    show()


main()
