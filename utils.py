import torch
from PIL import Image
import torch.nn.functional as F
import numpy as np

def euclidean_dist(x, y):
    '''
    Compute euclidean distance between two tensors
    '''
    # x: N x D
    # y: M x D
    n = x.size(0)
    m = y.size(0)
    d = x.size(1)
    if d != y.size(1):
        raise Exception

    x = x.unsqueeze(1).expand(n, m, d)
    y = y.unsqueeze(0).expand(n, m, d)

    return torch.pow(x - y, 2).sum(2)

def cosine_dist(x, y): # 效果不好
    return -torch.matmul(F.normalize(x), F.normalize(y).T)

def turn_img_white(img):
    if len(np.nonzero(img-255)) > img.size * 0.5: 
        img = 255 - img
        
def preprocess(img):
    # cut images white edges.
    # detect the character in the image and crop the character part
    img = np.array(img)
    
    # turn image to white background
    turn_img_white(img)
    
    # binarize 
    img = np.uint8((img > 128) * 255)

    # crop to square
    left, right, up, down = 10000, -1, 10000, -1
    h, w = img.shape
    for i in range(h):
        for j in range(w):
            if img[i, j] < 255:
                left = min(left, j)
                up = min(up, i)
                right = max(right, j)
                down = max(down, i)
    if not(left>=0 and right>=0 and up>=0 and down>=0):
        return Image.fromarray(img)
    if left >= right or up>=down:
        return Image.fromarray(img)
    vert_len = down - up
    hori_len = right - left
    width = max(vert_len, hori_len)
    new_img = np.ones((width, width))*255
    if vert_len > hori_len:
        hori_start = (vert_len - hori_len) // 2
        vert_start = 0
    else:
        vert_start = (hori_len - vert_len) // 2
        hori_start = 0
    new_img[vert_start:vert_start+vert_len, hori_start:hori_start+hori_len] = img[up:down, left:right]
    # binarize
    # new_img = np.uint8((new_img > 128) * 255)
    return Image.fromarray(new_img)
