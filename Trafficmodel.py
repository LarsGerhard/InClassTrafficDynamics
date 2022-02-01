# Imports
from numpy import array, linspace
from matplotlib.pyplot import figure, subplot, plot
from scipy.integrate import odeint

# Initial Variables (In mks units)
a = 0.7 # Acceleration
b = 2. # Deceleration
delta = 4. # Acceleration exponent
L = 5. # Vehicle length
xmin = 2. # Minimum gap
T = 1.8 # Time headway
vdes = 28 # Desired speed
Xblock = 5000 # Barrier position

# Initial Conditions
x0 = 0
v0 = 0
V = array([x0,v0])

# set the time interval for solving
t0 = 0
tf = Xblock / vdes

# Form Time array
t = linspace(t0,tf,400) # 400 steps for nice plot

def main():
    X = odeint(singleratefunc, V, t, tfirst=True)

    # unpack the results. In the output array, variables are columns, times are rows
    xout = X[:, 0]
    tout = X[:, 1]


    # For plotting
    fig = figure()

    ax1 = subplot()
    ax1.plot(t, xout, 'b')
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('distance (m)', color='b')
    ax1.tick_params('y', colors='b')

    ax2 = ax1.twinx()
    ax2.plot(t, tout, 'r')
    ax2.set_ylabel('velocity (m/s)', color='r')
    ax2.tick_params('y', colors='r')

    fig.tight_layout()

    plot()

# Differential Equation
def singleratefunc(t, V):
    # RATE_FUNC: IDM Car model
    # Model a car approaching a solid wall

    # unpack
    x = V[0]  # position
    v = V[1]  # velocity

    # Compute acceleration from IDM

    a_idm = a * (1 - (v / vdes)**delta)

    # compute derivatives
    dx = v
    dv = a_idm

    # pack rate array
    rate = array([dx, dv])
    return rate



main()


