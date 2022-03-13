# Imports
from numpy import linspace, sqrt, pi, concatenate, zeros
from numpy.random import choice
from matplotlib.pyplot import figure, subplot, show
from scipy.integrate import odeint

# Initial Variables (In mks units)
a = 0.5  # Acceleration
b = 3  # Deceleration
delta = 2.  # Acceleration exponent
LC = 5.  # Vehicle length
LB = 10.
xmin = 2.  # Minimum gap
T = 1.8  # Time headway
vdes = 28  # Desired speed
r = 100  # Radius of the roundabout
C = 2 * pi * r  # Circumference of the roundabout
ncars = 10  # Number of cars in our system
nbusses = 0 # Number of busses in our system
nvehicles = ncars + nbusses

# Initial Conditions

L = zeros(nvehicles)

count = 0

for i in range(nvehicles):
    if (i % int(nvehicles / ncars) == 0) and (count < nbusses):
        L[i] = LB
        count += 1
    else:
        L[i] = LC

x0 = linspace(0, C - 50, nvehicles)
v0 = zeros(nvehicles)
v0[0] = 2
V1 = concatenate((x0, v0))

# set the time interval for solving (in mks)
t0 = 0
tf = 35 * 60

# Form Time array
tspace = linspace(t0, tf, int(4. * tf / 10.))  # Uses given ratio of steps -> time to generate number of steps needed


def main():
    M = odeint(ratefunc, V1, tspace, tfirst=True)
    # unpack the results. In the output array, variables are columns, times are rows
    xout = M[:, :nvehicles]
    vout = M[:, nvehicles:]
    # For plotting
    plot(xout, vout, tspace)


# Differential Equation
def ratefunc(t, V):
    # RATE_FUNC: IDM Car model
    # Model a car approaching a solid wall

    # unpack
    x = V[:nvehicles]  # position
    v = V[nvehicles:]  # velocity
    dv = zeros(nvehicles)

    # Compute acceleration from IDM

    for i in range(nvehicles):
        if (i + 1) == nvehicles:
            s = (x[0] - L[i]) - (x[i] - C)
            deltav = (v[i] - v[0])

        else:
            s = ((x[i + 1] - L[i]) - x[i])
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
