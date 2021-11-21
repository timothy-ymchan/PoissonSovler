import numpy as np 
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import os
import h5py 
from datetime import datetime

# Parameters 
x1 = x2 = 1.0   # Size of plate
N1 = N2 = 100  # Grid points used
h = x1 / N1     # Grid size (Size x1=x2, only need to cal once)
v_top, v_bottom, v_left, v_right = 100, 0, 20, 80 # Boundary conditions
eps = 1e-4      # Uniform convergence 
cycle_limit = 15000 # Cycle limit
charge_on = False # Add charge to simulation

V_n = np.zeros(shape=(N1+2, N2+2)) # Current V[x][y] (The +2 defined the boundary)
V_p = np.zeros(shape=(N1+2,N2+2))  # Previous V[x][y] for convergence
rho = np.zeros(shape=(N1,N2))    # rho[x][y] (Since diff dim from V need to -1 in index)


# Initialize boundary conditions
for x in range(0,N1+2):          # Top and bottom boundaries
    V_n[x][0]    = v_bottom
    V_n[x][N2+1] = v_top
for y in range(0,N2+2):          # Left and right boundaries
    V_n[0][y]    = v_left
    V_n[N1+1][y] = v_right

if charge_on: # If add charge
    # Point charge 
    rho[int(N1/2)][int(N2/2)] = 1.0/(h*h*h)
    """
    # Intersting charge distribution
    for x in range(1,N1+1):
        for y in range(1,N2+1):
            x1,x2 = (x-1)/N1, (y-1)/N2   # Simulation coordinates
            rho[x-1][y-1] = (50.0/h)*np.sin(2*np.pi*(x1-0.5)*(x2-0.5))"""
    


np.copyto(V_p,V_n) # Make sure V_p also have those BCs

# Jacobi Scheme 
cycle = 0
while cycle < cycle_limit:

    # Iteration
    for x in range(1,N1+1):
        for y in range(1,N2+1):
            V_n[x][y] = 0.25*(V_p[x+1][y]+V_p[x-1][y]+V_p[x][y+1]+V_p[x][y-1] + h*h*rho[x-1][y-1])

    # Convergence
    max_eps = np.amax(np.abs(V_n-V_p)) # Find max{|V_n+1 - V_n|} for uniform convergence
    if max_eps < eps:
        break
    
    np.copyto(V_p,V_n)
    
    if (cycle + 1) % 100 == 0:
        print(f"Completed {cycle+1} cycles")
    cycle += 1 # Increment cycle count

print(f'Simulation complete (Cycle: {cycle})')


# Plotting
fig = plt.figure()
plot = fig.add_subplot(111,projection='3d')

X,Y = np.meshgrid(np.linspace(0,x1,N1+2),np.linspace(0,x2,N2+2))
plot.plot_surface(X,Y,V_n,cmap=cm.RdBu,antialiased=True)

plt.show()

# Save result
now = datetime.now().strftime(r'%H-%M-%S-%d-%m')
f = h5py.File(f'./poisson-{now}.hdf5','w')
result = f.create_group('result')
meta = f.create_group('metadata')

result['volt'] = V_n
result['rho'] = rho

meta['domain-size'] = (x1,x2)
meta['domain-div'] = (N1,N2)
meta['BCs'] = (v_top,v_bottom,v_left,v_right)
meta['eps'] = eps
meta['charge_on'] = charge_on

f.close()
