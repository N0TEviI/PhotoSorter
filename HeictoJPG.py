# HEIC to JPG image format batch conversion script for Python 3. Tested on Windows 10.
# You will need to have ImageMagick installed: https://www.imagemagick.org/

import os
import subprocess
import argparse
import logging
import config

logging.basicConfig(handlers=[logging.FileHandler(config.LOGFILE, 'w')],
                    level=logging.ERROR,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S', )


class HEIC(object):
    """HEIC图片处理类"""

    _copy_file = None

    def __init__(self, source_dir=None, save_dir=None) -> None:
        self._source_dir = source_dir
        self._save_dir = save_dir

        super().__init__()

    @property
    def copy_mode(self):
        return self._copy_file

    @copy_mode.setter
    def copy_mode(self, copy_mode):
        self._copy_file = copy_mode

    def __walk_files(self):
        if os.path.exists(self._source_dir):
            for dirpath, dirnames, filenames in os.walk(self._source_dir):
                for name in filenames:
                    filename = os.path.join(dirpath, name)
                    yield filename
        else:
            raise IOError('Path does not exist: {0}'.format(self._source_dir))

    def convertor(self):
        if not os.path.exists(self._save_dir):
            try:
                os.mkdir(self._save_dir)
            except IOError:
                raise IOError('Path does not create：{0}'.format(self._save_dir))

        for source_file in [filename for filename in self.__walk_files()
                            if os.path.splitext(filename)[1].lower() in config.HEICEXT]:
            save_file = os.path.join(self._save_dir, os.path.basename(source_file)[0:-5] + '.JPG')
            subprocess.run(["magick", "%s" % source_file, "%s" % save_file])
            if not self.copy_mode:
                os.remove(source_file)
            print('{0} -> {1}'.format(source_file, save_file))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('source_dir', help="HEIC待处理图片文件的路径，例如：c:\\source_dir")
    parser.add_argument('save_dir', help='转换为JPG文件存放的路径')
    parser.add_argument('-C', '--copy', help='复制文件，不删除原文件', action='store_true')
    parser.add_argument('-V', '--version', help='显示程序版本号', action='version', version='%(prog)s v1.0')

    args = parser.parse_args()

    _source_dir = args.source_dir
    _save_dir = args.save_dir
    _copy_file = bool(args.copy)

    heic = HEIC(_source_dir, _save_dir)
    heic.copy_mode = _copy_file
    heic.convertor()
    print('\nAll tasks have been completed.')
