'''
usage:
gif_imgs=[]
for z in np.arange(0,len(foo), step=1):
    plt.figure(figsize=(10,10))
    plt.title(f'z={z}')
    plt.imshow(foo[z])    
    
    buf = io.BytesIO()
    plt.savefig(buf, format='jpg')
    buf.seek(0)
    buf_r = buf.read()
    gif_imgs.append(buf_r)
    
gif = gif_from_pngs(gif_imgs, duration=600)
IPython.display.Image(gif)    

'''    

import io
import IPython

def bytes2PIL(s,**kwargs):
    import PIL
    with io.BytesIO() as f:
        f.write(s)
        f.seek(0)
        img=PIL.Image.open(f,**kwargs).copy()
    return img

def savefig_PIL(format='png',bbox_inches='tight',**kwargs):
    with io.BytesIO() as f:
        plt.gcf().savefig(f,format=format,bbox_inches=bbox_inches,**kwargs)
        f.seek(0)
        s=f.read()
    return s

def gif_from_pngs(pngs,duration=250):
    import PIL
    imgs=[bytes2PIL(x) for x in pngs]
    with io.BytesIO() as f:
        imgs[0].save(f,save_all=True,append_images=imgs[1:],
                duration=duration,loop=0,format='gif')
        f.seek(0)
        s=f.read()
    return s


def savefig_PIL(format='png',bbox_inches='tight',**kwargs):
    with io.BytesIO() as f:
        plt.gcf().savefig(f,format=format,bbox_inches=bbox_inches,**kwargs)
        f.seek(0)
        s=f.read()
    return s

