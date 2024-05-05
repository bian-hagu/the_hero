from PIL import Image, ImageOps
import os

def load_imgs(path):
  for imgname in sorted(os.listdir(path)):
    im = Image.open(path + '/' + imgname)
    im_mirror = ImageOps.mirror(im)
    im_mirror.save(path + '/' + imgname)
load_imgs('data/imgs/entities/slime/slime_death')