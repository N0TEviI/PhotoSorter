# /usr/bin/env python
# -*- coding: utf-8 -*-
# Date:2017/8/5 11:16
# __author__ = 'P0WER1ISA'
# __homepage__ = 'https://github.com/P0WER1ISA'

class PhotoSorter(object):
    """定义类"""

    # 待处理文件夹
    _input_dir = None
    # 归档后输出文件夹
    _output_dir = None

    def __init__(self, input_dir, output_dir) -> None:
        self._input_dir = input_dir
        self._output_dir = output_dir

        super().__init__()

    @property
    def input_dir(self):
        return self._input_dir

    @property
    def output_dir(self):
        return self._output_dir


if __name__ == "__main__":
    input_dir = 'Z:\Pictures'
    output_dir = 'Z:\OutputDir'

    ps = PhotoSorter(input_dir, output_dir)
    print(ps.input_dir)