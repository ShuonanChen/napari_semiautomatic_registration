import numpy as np


def trans(source,T_dict,o_shape):  # original when source image is of size (c,z,x,y)
    assert(len(source.shape)==4)  # this is (c,z,x,y) where c==2 for now. z can be 8,16,24....
    C = source.shape[0]
    B = np.eye(4)
    for l in T_dict:
        for k,v in l.items():
            if k=='bhat':
                B = B@((np.c_[v, np.array((0,0,0,1))]))
            if k=='scale':
                B[:,:3] *= v  
    R_3 = (np.linalg.inv(B[:3,:3])).T
    offset_3 = -B[-1,:-1]@np.linalg.inv(B[:3,:3])
    print('running rigid..')
    transformed_all = np.array([ndi.affine_transform(source[c].astype('float32'), R_3, offset = offset_3,
                                    output_shape = o_shape, order=1) for c in range(C)])
    return(transformed_all)



def wahba(X,Y):
    ''' 3d version'''
    X0=X-np.mean(X,axis=0)    
    Y0=Y-np.mean(Y,axis=0)    
    U, _, Vt = np.linalg.svd(X0.T@Y0)
    V = Vt.T
    M = np.eye(3)
    M[-1,:] = np.array((0,0,np.linalg.det(U)*np.linalg.det(V)))
    R = U@M@V.T
    T = np.mean(Y-X@R, axis = 0)
    return(np.r_[R,T[None,:]])  # return 4x3 matrix (to transform from first input to second inpupt)





def pad3d(a,out_shape):
    assert(len(a.shape)==3)
    assert(len(a.shape)==len(out_shape))    
    if np.product((np.array(out_shape)-np.array(a.shape))>=0)==0:        
        out =a[:out_shape[0],:out_shape[1],::out_shape[2]]
    else:
        print("the outshape is actually smaller than the input, we need to crop the original instead")
        out = np.zeros(out_shape)
        out[:a.shape[0], :a.shape[1],:a.shape[2]] = a
    return out


def pad2d(a,out_shape):
    """
    Return bottom right padding.
    assuming a is a 2-d array for now. 
    """
    assert(len(a.shape)==2)
    assert(len(a.shape)==len(out_shape))    
    if np.product((np.array(out_shape)-np.array(a.shape))>0)==0:        
        out =a[:out_shape[0],:out_shape[1]]
    else:
        print("the outshape is actually smaller than the input, we need to crop the original instead")
        out = np.zeros(out_shape)
        out[:a.shape[0], :a.shape[1]] = a
    return out



def pad_2d(a,o_shape):
    assert(len(a.shape)==2)
    out = np.zeros(o_shape)
    if ((a.shape-np.array(o_shape))>=0).all():  # crop on both axis
        out = a[:o_shape[0],:o_shape[1]]
    elif ((a.shape-np.array(o_shape))<0).all():  # pad with zero on both axis    
        out[:a.shape[0],:a.shape[1]] = a
    elif a.shape[0]>=o_shape[0]: # crop on x axis. 
        assert(a.shape[1]<o_shape[1])
        out = np.zeros(o_shape)
        out[:,:a.shape[1]] = a[:o_shape[0]]
    elif a.shape[0]<o_shape[0]: # crop on y axis. 
        assert(a.shape[1]>=o_shape[1])
        out[:a.shape[0],:] = a[:,:o_shape[1]]
    return out