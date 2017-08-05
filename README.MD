# PhotoSorter
___
> author：P0WER1ISA

> homepage：[https://github.com/P0WER1ISA/PhotoSorter](https://github.com/P0WER1ISA)

> description：软件读取图片ＥＸＩＦ信息，按照日期来进行文件夹方式归档
___

### Usage：
<pre>
(venv) D:\Documents\PycharmProjects\PhotoSorter>python photosorter.py -h
usage: photosorter.py [-h] [-M MODE] [-C] [-R] [-V] source_dir save_dir

positional arguments:
  source_dir            待处理图片文件的路径，例如：C:\Photos
  save_dir              归档后的文件存放路径

optional arguments:
  -h, --help            show this help message and exit
  -M MODE, --mode MODE  图片文件按照年份(year)、月份(month)、日期(day)，进行归档，默认是月份
  -C, --copy            复制文件，不删除原文件
  -R, --rename          文件是否按照日期重命名
  -V, --version         显示程序版本号
</pre>


### Ex：
![](https://raw.githubusercontent.com/P0WER1ISA/PhotoSorter/master/screenshots/1.png)
 
 
![](https://raw.githubusercontent.com/P0WER1ISA/PhotoSorter/master/screenshots/2.png)


![](https://raw.githubusercontent.com/P0WER1ISA/PhotoSorter/master/screenshots/3.png)


![](https://raw.githubusercontent.com/P0WER1ISA/PhotoSorter/master/screenshots/4.png)