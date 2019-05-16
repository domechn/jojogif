import cv2
import random
import string
import shutil
import tempfile
from os import path,  listdir
import imageio
from utils import *

_random_dir_name_len = 10
_to_be_continued_path = 'image/to_be_continued.jpg'


class VideoService():

    def __init__(self, pt: str, begin, end: float, width, height: int):
        if not end:
            end = 20
        self._path = pt
        self._begin = begin
        self._end = end
        self._width = 0
        self._height = 0
        if width:
            self._width = width
        if height:
            self._height = height
        self._to_dir = path.join(
            tempfile.gettempdir(), 'jojogif',
            ''.join(random.sample(string.ascii_letters + string.digits,
                                  _random_dir_name_len)))

    def to_images(self):
        c = 0
        print_step('begin to make video to images')
        make_dir_nx(self._to_dir)
        try:
            vc = cv2.VideoCapture(self._path)
            if vc.isOpened():
                width = self._width or vc.get(cv2.CAP_PROP_FRAME_WIDTH)
                height = self._height or vc.get(cv2.CAP_PROP_FRAME_HEIGHT)
                fps = vc.get(cv2.CAP_PROP_FPS)
                timeF = int(fps / 10)
            else:
                raise RuntimeError("cannot open video")
            while True:
                rval, frame = vc.read()
                if frame is None:
                    break
                c += 1
                if c < self._begin * fps:
                    continue
                if c > self._end * fps:
                    break
                if c % timeF == 0:
                    frame = cv2.resize(
                        frame, (int(width * 0.5), int(height * 0.5)))
                    cv2.imwrite(f'{self._to_dir}/{c}.jpg', frame)
                cv2.waitKey(1)
        finally:
            vc.release()
        print_step('make video to images successfully')

    def to_gif(self, jojo: bool, out_path: str):
        def get_image_path(p: str) -> str:
            return path.join(self._to_dir, p)

        ls = listdir(self._to_dir)
        ls.sort(key=lambda x: int(x.split('.')[0]))

        if out_path.endswith('.gif'):
            outfilename = out_path
        else:
            outfilename = path.join(out_path, 'test.gif')

        if jojo:
            # con_image = cv2.imread(_to_be_continued_path)
            last_image_path = get_image_path(ls[len(ls)-1])
            last_image = cv2.imread(last_image_path)
            last_image_grey = cv2.cvtColor(last_image, cv2.COLOR_RGB2GRAY)
            last_image_blur = cv2.GaussianBlur(last_image_grey, (5, 5), 0)
            temp_last_name = ls[len(ls)-1]
            for i in range(10):
                name = get_image_path(
                    add_number_file_name(temp_last_name, i+1))
                cv2.imwrite(name, last_image_grey)
                ls.append(name)

        frames = [imageio.imread(get_image_path(image_name))
                  for image_name in ls]

        try:
            imageio.mimsave(outfilename, frames, 'GIF')
        finally:
            rm_dir_f(self._to_dir)

