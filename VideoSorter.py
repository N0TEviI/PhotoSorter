# /usr/bin/env python
# -*- coding: utf-8 -*-
# Date:2017/8/5 11:16
# __author__ = 'P0WER1ISA'
# __homepage__ = 'https://github.com/P0WER1ISA'
from datetime import datetime
import os
from multiprocessing import Process
import argparse
import shutil
import logging
import config

logging.basicConfig(handlers=[logging.FileHandler(config.LOGFILE, 'w')],
                    level=logging.ERROR,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S', )


class VideoSorter(object):
    """图片处理类"""

    _save_mode = None
    _copy_file = None
    _rename_file = None
    _counter = 0

    def __init__(self, source_dir=None, save_dir=None) -> None:
        """初始化"""
        self._source_dir = source_dir
        self._save_dir = save_dir

        super().__init__()

    @property
    def save_mode(self):
        return self._save_mode

    @save_mode.setter
    def save_mode(self, save_mode):
        self._save_mode = save_mode

    @property
    def copy_mode(self):
        return self._copy_file

    @copy_mode.setter
    def copy_mode(self, copy_mode):
        self._copy_file = copy_mode

    @property
    def rename_file(self):
        return self._rename_file

    @rename_file.setter
    def rename_file(self, rename_file):
        self._rename_file = rename_file

    @staticmethod
    def get_video_timestamps(filename):
        ''' Get the creation and modification date-time from .mov metadata.

            Returns None if a value is not available.
        '''
        from datetime import datetime as DateTime
        import struct

        ATOM_HEADER_SIZE = 8
        # difference between Unix epoch and QuickTime epoch, in seconds
        EPOCH_ADJUSTER = 2082844800

        creation_time = modification_time = None

        # search for moov item
        with open(filename, "rb") as f:
            while True:
                atom_header = f.read(ATOM_HEADER_SIZE)
                # ~ print('atom header:', atom_header)  # debug purposes
                if atom_header[4:8] == b'moov':
                    break  # found
                else:
                    atom_size = struct.unpack('>I', atom_header[0:4])[0]
                    f.seek(atom_size - 8, 1)

            # found 'moov', look for 'mvhd' and timestamps
            atom_header = f.read(ATOM_HEADER_SIZE)
            if atom_header[4:8] == b'cmov':
                raise RuntimeError('moov atom is compressed')
            elif atom_header[4:8] != b'mvhd':
                raise RuntimeError('expected to find "mvhd" header.')
            else:
                f.seek(4, 1)
                creation_time = struct.unpack('>I', f.read(4))[0] - EPOCH_ADJUSTER
                creation_time = DateTime.fromtimestamp(creation_time)
                if creation_time.year < 1990:  # invalid or censored data
                    creation_time = None

                modification_time = struct.unpack('>I', f.read(4))[0] - EPOCH_ADJUSTER
                modification_time = DateTime.fromtimestamp(modification_time)
                if modification_time.year < 1990:  # invalid or censored data
                    modification_time = None

        return creation_time, modification_time

    def run(self):
        """程序入口"""
        for fname in [filename for filename in self.__walk_files() if
                      os.path.splitext(filename)[1].lower() in config.VIDEOEXT]:
            file_ext = os.path.splitext(fname)[1].lower()

            try:
                datetime_original, _ = self.get_video_timestamps(fname)
            except Exception as e:
                datetime_original = None

            save_dir, save_filename_without_ext = self.__get_output_dir_filename(datetime_original)
            if self.rename_file:
                save_filename = save_filename_without_ext + file_ext
            else:
                save_filename = os.path.basename(fname)

            self._counter += 1
            p = Process(target=VideoSorter._save_file,
                        args=(self._counter, self._copy_file, fname, save_dir, save_filename))
            p.start()
            p.join()

    def __walk_files(self):
        """递归批量返回待处理文件"""
        if os.path.exists(self._source_dir):
            for dirpath, dirnames, filenames in os.walk(self._source_dir):
                for name in filenames:
                    filename = os.path.join(dirpath, name)
                    yield filename
        else:
            raise IOError('Path does not exist: {0}'.format(self._source_dir))

    @staticmethod
    def _save_file(counter, copy_file, source_file, save_dir, save_filename):
        """
        保存文件
        :param counter:计数器
        :param copy_file:复制模式
        :param source_file:原文件
        :param save_dir:目标文件夹
        :param save_filename:目标文件名
        :return:
        """
        if not os.path.exists(save_dir):
            try:
                os.makedirs(save_dir)
            except IOError:
                raise IOError('Path does not create：{0}'.format(save_dir))
        save_file = os.path.join(save_dir, save_filename)
        if copy_file:
            shutil.copyfile(source_file, save_file)
        else:
            shutil.move(source_file, save_file)

        print('{0} >>> source:{1} -> to:{2}'.format(counter, source_file, save_file))

    def __get_output_dir_filename(self, datetime_original):
        """
        根据文件创建时间返回文件的存放路径
        :param datetime_original:
        :return:
        """
        # 初始化年月日
        year, month, day = datetime.min.year, datetime.min.month, datetime.min.day
        # 初始化时分秒
        hour, minute, second = datetime.now().hour, datetime.now().minute, datetime.now().second
        if datetime_original is not None:
            try:
                # 转换datetime_original，得到年月日时分秒
                t = datetime.strptime(str(datetime_original), '%Y-%m-%d %H:%M:%S')
                year, month, day = t.year, t.month, t.day
                hour, minute, second = t.hour, t.minute, t.second
            except Exception as e:
                logging.error('Error message:{0}.'.format(e))
        if self.save_mode == 'year':
            # 按照年份保存
            return os.path.join(self._save_dir, str(year)), ''.join(
                [str(year), str(month), str(day), str(hour), str(minute), str(second)])
        elif self.save_mode == 'month':
            # 按照年份月份保存
            return os.path.join(self._save_dir, str(year), str(month)), ''.join(
                [str(year), str(month), str(day), str(hour), str(minute), str(second)])
        elif self.save_mode == 'day':
            # 按照年份月份日期保存
            return os.path.join(self._save_dir, str(year), str(month), str(day)), ''.join(
                [str(year), str(month), str(day), str(hour), str(minute), str(second)])
        else:
            raise ValueError('Save_mode is error:\'{0}\'.'.format(self.save_mode))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('source_dir', help='待处理视频文件的路径，例如：c:\\source_dir')
    parser.add_argument('save_dir', help='归档后的文件存放路径')
    parser.add_argument('-M', '--mode', help='视频文件按照年份(year)、月份(month)、日期(day)，进行归档，默认是月份', default='month')
    parser.add_argument('-C', '--copy', help='复制文件，不删除原文件', action='store_true')
    parser.add_argument('-R', '--rename', help='文件是否按照日期重命名', action='store_true')
    parser.add_argument('-V', '--version', help='显示程序版本号', action='version', version='%(prog)s v1.0')
    args = parser.parse_args()

    _source_dir = args.source_dir
    _save_dir = args.save_dir
    if args.mode in ('year', 'month', 'day'):
        _save_mode = args.mode
    else:
        _save_mode = 'month'
    _copy_file = bool(args.copy)
    _rename_file = bool(args.rename)

    ps = VideoSorter(_source_dir, _save_dir)
    ps.save_mode = _save_mode
    ps.copy_mode = _copy_file
    ps.rename_file = _rename_file

    ps.run()
    print('\nAll tasks have been completed.')
