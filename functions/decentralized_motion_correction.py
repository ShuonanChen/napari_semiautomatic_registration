from scipy import sparse
import numpy as np
import simplemocor  # utility code from the local
import registration
# from skimage.registration import phase_cross_correlation


def get_D(data,r=10,z_r=3):    
    assert(len(data.shape)==3)
    D_x = np.empty((len(data),len(data))); D_x[:] = np.nan
    D_y = np.empty((len(data),len(data))); D_y[:] = np.nan

#     M = np.zeros((len(data),len(data)), dtype = bool)  # mask
    for i in np.arange(len(data)-1, step=1):
        for j in np.arange(i-z_r+1,i+z_r,step=1):
            if j >= len(data) or j < 0:
                continue;
            optings=simplemocor.normcor(data[i],data[j][r:-r, r:-r])    # move j-th image to teh i-th image
            best_shift=np.unravel_index(np.argmax(optings),optings.shape) - np.array((r,r)).astype(int)
            D_x[i,j] = best_shift[0]
            D_y[i,j] = best_shift[1]
#             M[i,j]=True
#     mask = M.copy()
    return(D_x,D_y)



def decentralized_reg_solve_p(D):
    '''
    M is the mask (S in the original paper)
    D is the distance matrix 
    '''
    V=D[~np.isnan(D)]
    I,J = np.where(~np.isnan(D))
    M=sparse.csr_matrix((np.ones(len(I)), (np.arange(0,len(I)).T,I)), shape = (len(I),len(D)));
    N=sparse.csr_matrix((np.ones(len(J)), (np.arange(0,len(J)).T,J)), shape = (len(I),len(D)));
    A=M-N;
    p = -sparse.linalg.lsqr(A,V[:,None])[0]
    return(p)
    
    
    
def correctmotion(data):    
    D_x, D_y = get_D(data)
    p_x  = decentralized_reg_solve_p(D_x)
    p_y  = decentralized_reg_solve_p(D_y)
    rez = data.copy()
    for z in np.arange(len(data), step=1):
        rez[z] = registration.roll_shift(rez[z], (np.around(p_x[z]).astype(int), np.around(p_y[z]).astype(int)))
    return(rez)