import numpy as np
from mpi4py import MPI
from pyutils.ctutils.driver.chem_uq import counterflow_premixed_extinction

# parallel init
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

n = 25

data = counterflow_premixed_extinction(
    n, 'H2', T=300, p=1013250., phi=0.6,
    a_init=1000., a_max=1E+6, L_init=0.01,
    folder_name='tmp_{:g}'.format(rank))

# data collection
data = comm.gather(data, root=0)

if rank == 0:
    with open('counterflow_premixed.dat','w') as f:
        for ds in data:
            for d in ds:
                np.savetxt(f, [d[0]], fmt='%.3e')
                np.savetxt(f, [d[1]], fmt='%.3e')
