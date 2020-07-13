import random
import string
import tempfile
from base64 import b64decode

import cv2
import numpy as np
import imageio
from os import listdir
from utils import *
from common import logo_base64

_random_dir_name_len = 10
_to_be_continued_path = 'image/to_be_continued.png'


class VideoService():

    def __init__(self, pt: str, begin: float, end: float, width, height, intended_fps: int):
        if not end:
            end = 20  # default: 20s
        self._path = pt
        self._begin = begin
        self._end = end
        self._width = width or 0
        self._height = height or 0
        self._intended_fps = intended_fps
        self._to_dir = path.join(
            tempfile.gettempdir(), 'jojogif',
            ''.join(random.sample(string.ascii_letters + string.digits,
                                  _random_dir_name_len)))

    def to_images(self):
        '''
        Convert video to picture
        '''
        c = 0
        print_step('begin to make video to images')
        make_dir_nx(self._to_dir)
        try:
            vc = cv2.VideoCapture(self._path)
            if vc.isOpened():
                width = self._width or vc.get(cv2.CAP_PROP_FRAME_WIDTH)
                height = self._height or vc.get(cv2.CAP_PROP_FRAME_HEIGHT)
                source_fps = vc.get(cv2.CAP_PROP_FPS)

                timeF = round(source_fps / self._intended_fps) or 1
                self._true_fps = source_fps / timeF
                self._gif_delay = 1 / self._true_fps

            else:
                raise RuntimeError("cannot open video")
            while True:
                rval, frame = vc.read()
                if frame is None:
                    break
                c += 1
                if c < self._begin * source_fps:
                    continue
                if c > self._end * source_fps:
                    break
                if c % timeF == 0:
                    frame = cv2.resize(
                        frame, (int(width), int(height)), interpolation=cv2.INTER_AREA)

                    cv2.imwrite(f'{self._to_dir}/{c}.jpg', frame)
                cv2.waitKey(1)
        finally:
            vc.release()
        print_step('make video to images successfully')

    def to_gif(self, jojo: bool, out_path: str):
        '''
        Convert video to picture
        '''
        def get_image_path(p: str) -> str:
            return path.join(self._to_dir, p)

        ls = listdir(self._to_dir)
        ls.sort(key=lambda x: int(x.split('.')[0]))

        if out_path.endswith('.gif'):
            outfilename = out_path
        else:
            fn = get_file_name(self._path)
            outfilename = path.join(out_path, f'{fn}.gif')
        dir_path = path.split(outfilename)[0]
        if not path.exists(dir_path):
            makedirs(dir_path)
        try:
            if jojo:
                ls = np.append(ls, self.add_tbc_logo(ls[-1], get_image_path))
                # ls.append(self.add_tbc_logo(ls[-1], get_image_path))

            frames = [imageio.imread(get_image_path(image_name))
                      for image_name in ls]
            imageio.mimsave(outfilename, frames, 'GIF', duration=self._gif_delay)
        finally:
            rm_dir_f(self._to_dir)
            print_step('true fps: %d' % round(self._true_fps))

    def add_tbc_logo(self, last_image_name, get_image_path) -> list:
        '''
        add to be continued logo to the left-bottom of the image
        return: the name of all translated images
        '''
        img_data = b64decode(logo_base64)
        img_array = np.frombuffer(img_data, np.uint8)  # 转换np序列
        con_image = cv2.imdecode(img_array, -1)
        self.blur_last_image(get_image_path(last_image_name))
        tp = cv2.imread(self._temp_file)
        res = list()
        for i in range(round(self._true_fps)): # tbc image appears for about 1 second
            name = get_image_path(
                add_number_file_name(last_image_name, i+1))
            cv2.imwrite(name, self.cover(con_image, tp))
            res.append(name)
        return res

    def blur_last_image(self, p: str):
        last_image = cv2.imread(p)
        last_image_grey = cv2.cvtColor(last_image, cv2.COLOR_RGB2GRAY)
        last_image_blur = cv2.GaussianBlur(last_image_grey, (5, 5), 0)
        temp_file_path = path.join(self._to_dir, 'temp_file.jpg')
        self._temp_file = temp_file_path
        cv2.imwrite(temp_file_path, last_image_blur)

    def cover(self, s_img, l_img, x_offset=0, y_offset=0):
        '''
        Overlay the s_image on the l_img
        '''
        l_height, l_width = l_img.shape[0], l_img.shape[1]
        s_img = cv2.resize(s_img, (int(l_width*0.5), int(l_height*0.3)))
        x_offset = int(l_width * 0.1)
        y_offset = int(l_height * 0.7)
        y1, y2 = y_offset, y_offset + s_img.shape[0]
        x1, x2 = x_offset, x_offset + s_img.shape[1]

        alpha_s = s_img[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        for c in range(3):
            l_img[y1:y2, x1:x2, c] = (alpha_s * s_img[:, :, c] +
                                      alpha_l * l_img[y1:y2, x1:x2, c])
        return l_img
