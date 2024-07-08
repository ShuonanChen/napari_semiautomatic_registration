import numpy as np
import numpy as np
import scipy as sp
import scipy.misc
import scipy.signal
import scipy.ndimage
import math
    
def unif_filt1_valid(A,m,axis=0):
    if m>1:
        A=np.swapaxes(A,axis,0)
        if m%2==0:
            A=sp.ndimage.uniform_filter1d(A,m,axis=0)[m//2:A.shape[0]-m//2+1]*m
        else:
            A=sp.ndimage.uniform_filter1d(A,m,axis=0)[m//2:A.shape[0]-m//2]*m
        A=np.swapaxes(A,axis,0)
        return A
    else:
        return A
    
def unif_filt_valid(A,m):
    for i,v in enumerate(m):
        A=unif_filt1_valid(A,v,i)
        
    return A
    

def normcor(X,Y):  
    '''
    X is a big array
    Y is a smaller array (moving)
    
    For each valid placement of Y inside X, we want to compute
    the normalized correlation between Y and the X pixels where Y is placed
    '''

    X=np.require(X,dtype=np.float)
    Y=np.require(Y,dtype=np.float)

    for i in range(len(X.shape)):
        assert X.shape[i]>=Y.shape[i]
    
    # normalize Y
    Y=Y-np.mean(Y)
    Y=Y/np.linalg.norm(Y)
    
    # get the number of pix
    NN=np.prod(Y.shape)
    
    # for each valid placement rgn, get sum x_i
    # sums=sp.signal.fftconvolve(X,np.ones(Y.shape),'valid')
    sums=unif_filt_valid(X,Y.shape)
    
    # for each valid placement rgn, get sum x_i**2
    # sums2=sp.signal.fftconvolve(X**2,np.ones(Y.shape),'valid')
    sums2=unif_filt_valid(X**2,Y.shape)
    
    # for each valid placement rgn, get sum x_i*y_i
    sl=tuple([slice(None,None,-1) for i in range(len(Y.shape))])
    dots=sp.signal.fftconvolve(X,Y[sl],mode='valid')
    
    # for each valid placement rgn, get vr_i
    '''
    Want: 
    
      sum (x_i - rgnmean)**2
    = sum x_i**2 + rgnmean**2 - 2*x_i*rgnmean
    = sums2 + NN*(rgnmean**2) - 2*sums*rgnmean
    = sums2 + (sums**2)/NN - 2*sums*sums/NN
    = sums2 - sums*sums/NN
    '''
    normsq = sums2 - (sums**2)/NN
    norms = np.sqrt(normsq)
    
    # for each valid placement rgn, get |X-Y|
    '''
    Want
      sum y_i * (x_i - rgnmean)/norms
    = (sum y_i * x_i)/norms - sumsy*rgnmean/norms
    = (sum y_i * x_i)/norms - sumsy*rgnmean/norms
    '''
    cos = dots /norms
    
    return cos




def roll(A,s,axis):
    A=np.swapaxes(A,axis,0)    
    A=np.roll(A,s,axis=0)    
    if s<0:
        A[s:]=0
    else:
        A[:s]=0                
    A=np.swapaxes(A,axis,0)    
    return A

def roll_shift(A,s):
    for i,x in enumerate(s):
        A=roll(A,x,axis=i)
    return A


def normalize(x):
    img2 = np.max(x,0)
    img2 -= img2.min()
    img2 /=img2.max()
    return(img2)

def learn_shift(im1,im2):
    optings=normcor(im1,im2)  
    out=np.array(np.unravel_index(np.argmax(optings),optings.shape))
    return(out)

def get_R_from_a(a):
    R = np.eye(3)
    R[0] = np.array((math.cos(a),-math.sin(a),0))
    R[1] = np.array((math.sin(a),math.cos(a),0))
    return(R)
