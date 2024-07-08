import numpy as np



def gray2RGB(img, col, scl = 1):  ## updated version
    cols = ['r','g','b','y','m','cyan','white','purple','pink', 'orange']
    if len(img.shape)==3:
        img = np.max(img,axis=0)
    assert(len(img.shape)==2)
    colid = np.where(np.array([col==c for c in cols]))[0][0]    
    img_rgb = np.zeros(img.shape+(3,))
    if colid <3: # RGB case:        
        img_rgb[:,:,colid] = img.copy()
    else:
        if col=='y': # if its yellow, 
            img_rgb[:,:,0] = img.copy()
            img_rgb[:,:,1] = img.copy()
            img_rgb[:,:,2] = img.copy()*0
        if col=='m': # magenta case,
            img_rgb[:,:,0] = img.copy()
            img_rgb[:,:,2] = img.copy()
        if col=='cyan': # cyan
            img_rgb[:,:,1] = img.copy()
            img_rgb[:,:,2] = img.copy()
    img_rgb /=img_rgb.max()*scl
    return(img_rgb)    

