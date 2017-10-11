# coding=utf-8
import os
import logging
import logging.handlers

path_lst = __file__.split(os.sep)
while True:
    if path_lst[-1] == 'Alpha':
        break
    path_lst = path_lst[:-1]
# logDir = r"D:\logs"
log_dir = os.sep.join(path_lst+['logs', 'workers', 'preprocess'])

logName = os.path.join(log_dir, 'info.log')


# 创建一个logger实例
logger = logging.getLogger()
logger.setLevel("DEBUG")  # 设置级别为DEBUG，覆盖掉默认级别WARNING
# 创建一个handler,用于写入日志文件，handler可以把日志内容写到不同的地方

fh = logging.FileHandler(logName)
fh.setLevel("DEBUG")
# 再创建一个handler，用于输出控制台
ch = logging.StreamHandler()
ch.setLevel("DEBUG")
# 定义handler的格式输出
log_format = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-[%(filename)s:%(lineno)d]::%(message)s")
fh.setFormatter(log_format)  # setFormatter() selects a Formatter object for this handler to use
ch.setFormatter(log_format)
# 为logger添加handler
logger.addHandler(fh)
logger.addHandler(ch)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++

check_log_name = os.path.join(log_dir, 'check.log')
check_logger = logging.getLogger('check')
check_logger.setLevel("DEBUG")
c_fh = logging.FileHandler(check_log_name)
c_fh.setLevel("DEBUG")
c_ch = logging.StreamHandler()
c_ch.setLevel("DEBUG")
# 定义handler的格式输出
# log_format = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-[%(filename)s:%(lineno)d]::%(message)s")
c_fh.setFormatter(log_format)  # setFormatter() selects a Formatter object for this handler to use
c_ch.setFormatter(log_format)
# 为logger添加handler
check_logger.addHandler(c_fh)
check_logger.addHandler(c_ch)


