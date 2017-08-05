# /usr/bin/env python
# -*- coding: utf-8 -*-
# Date:2017/8/5 11:16
# __author__ = 'P0WER1ISA'
# __homepage__ = 'https://github.com/P0WER1ISA'
import os
import argparse
import shutil
import logging
import config

logging.basicConfig(handlers=[logging.FileHandler(config.LOGFILE, 'w')],
                    level=logging.ERROR,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S', )
from datetime import datetime
import exifread


class PhotoSorter(object):
    """定义类"""

    # 待处理文件夹
    _source_dir = None
    # 归档后输出文件夹
    _save_dir = None
    # 文档按照年、月、日存储
    _save_mode = None
    # 采用复制模式，否则删除原有文件
    _copy_file = None
    # 是否以时间方式重命名文件
    _rename_file = None

    def __init__(self, source_dir=None, save_dir=None, save_mode=None, copy_file=None, rename_file=None) -> None:
        self._source_dir = source_dir
        self._save_dir = save_dir
        self._save_mode = save_mode
        self._copy_file = copy_file
        self._rename_file = rename_file

        super().__init__()

    @property
    def input_dir(self):
        return self._source_dir

    @property
    def output_dir(self):
        return self._save_dir

    @property
    def save_mode(self):
        return self._save_mode

    @property
    def copy_mode(self):
        return self._copy_file

    @property
    def rename_file(self):
        return self._rename_file

    def dispose(self):
        """得到所有需要处理的文件"""
        if os.path.exists(self.input_dir):
            for root, dirs, files in os.walk(self.input_dir):
                for name in files:
                    filename = os.path.join(root, name)
                    if os.path.isfile(filename) and os.path.splitext(filename)[1] in config.PHOTOEXT:
                        with open(filename, 'rb') as f:
                            tags = exifread.process_file(f)
                            try:
                                self.__save_file(filename, tags['EXIF DateTimeOriginal'])
                            except KeyError:
                                self.__save_file(filename, None)
                            except Exception as e:
                                logging.error('Error message:{0}.'.format(e))
                                raise e
        else:
            raise IOError('Path does not exist: {0}'.format(self.input_dir))

    def __save_file(self, filename, datetime_original):
        save_filepath, save_filename = self.__get_output_dir(datetime_original)

        if self.rename_file:
            save_filename = ''.join([save_filename, os.path.splitext(filename)[1]])
        else:
            save_filename = os.path.basename(filename)
        print('source:{0}   --->    to:{1}'.format(filename, save_filename))
        if not os.path.exists(save_filepath):
            try:
                os.makedirs(save_filepath)
            except:
                raise IOError('Path does not create：{0}'.format(save_filepath))
        if self.copy_mode:
            shutil.copyfile(filename, os.path.join(save_filepath, save_filename))
        else:
            shutil.move(filename, os.path.join(save_filepath, save_filename))

    def __get_output_dir(self, datetime_original) -> tuple:
        year, month, day = datetime.min.year, datetime.min.month, datetime.min.day
        hour, minute, second = datetime.now().hour, datetime.now().minute, datetime.now().second
        try:
            t = datetime.strptime(str(datetime_original), '%Y:%m:%d %H:%M:%S')
            year, month, day = t.year, t.month, t.day
            hour, minute, second = t.hour, t.minute, t.second
        except Exception as e:
            logging.error('Error message:{0}.'.format(e))
        if self.save_mode == 'year':
            return os.path.join(self.output_dir, str(year)), ''.join(
                [str(year), str(month), str(day), str(hour), str(minute), str(second)])
        elif self.save_mode == 'month':
            return os.path.join(self.output_dir, str(year), str(month)), ''.join(
                [str(year), str(month), str(day), str(hour), str(minute), str(second)])
        elif self.save_mode == 'day':
            return os.path.join(self.output_dir, str(year), str(month), str(day)), ''.join(
                [str(year), str(month), str(day), str(hour), str(minute), str(second)])
        else:
            raise ValueError(
                'Save_mode is error:\'{0}\'.'.format(self.save_mode))


# ''.join(str(hour), str(minute), str(second)
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('source_dir', help='待处理图片文件的路径，例如：C:\\Photos')
    parser.add_argument('save_dir', help='归档后的文件存放路径')
    parser.add_argument('-M', '--mode', help='图片文件按照年份(year)、月份(month)、日期(day)，进行归档，默认是月份', default='month')
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

    ps = PhotoSorter(_source_dir, _save_dir, _save_mode, _copy_file, _rename_file)
    ps.dispose()
