'''
增量备份，完全备份
完全备份时，将目录打个tar包，计算每个文件的md5值
增量备份时，备份有变化的文件和新增加的文件，更新md5值
'''

import time
import os
import tarfile
import pickle
import hashlib


def check_md5(filename):
    m = hashlib.md5()
    with open(filename, 'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data)
    return m.hexdigest()

def full_backup(scr_dir, dst_dir, md5file):
    filename = os.path.basename(scr_dir.strip('/'))
    filename = '%s_full_%s.tar.gz' % (filename, time.strftime('%Y%m%d'))
    filename = os.path.join(dst_dir, filename)
    md5dict = {}

    tar = tarfile.open(filename, 'w:gz')
    tar.add(scr_dir)
    tar.close()

    # 遍历被打包的目录计算文件MD5值
    for path, folders, files in os.walk(scr_dir):
        for each_file in files:
            key = os.path.join(path, each_file)
            md5dict[key] = check_md5(key)

    # 将字典写入文件中 使用pickle模块
    with open(md5file, 'wb') as fobj:
        pickle.dump(md5dict, fobj)

def incr_backup(scr_dir, dst_dir, md5file):
    filename = os.path.basename(scr_dir.strip('/'))
    filename = '%s_incr_%s' % (filename, time.strftime('%Y%m%d'))
    filename = os.path.join(dst_dir, filename)
    md5dict = {}

    # 提取老的md5值
    with open(md5file, 'rb') as fobj:
        oldmd5 = pickle.load(fobj)

    # 计算新的md5值
    for path, folders, files in os.walk(scr_dir):
        for each_file in files:
            key = os.path.join(path, each_file)
            md5dict[key] = check_md5(key)
    
    # 打包
    tar = tarfile.open(filename, 'w:gz')
    # 比较新旧md5值 有变化的备份
    for key in md5dict:
        if oldmd5.get(key) != md5dict[key]:
            tar.add(key)
    tar.close()


if __name__ == "__main__":
    # 需要打包的目录
    scr_dir = '/Users/zhonglinhui/Study/operational-tool'
    # 打包完存放的目录 mkdir /Users/zhonglinhui/Study/backup
    dst_dir = '/Users/zhonglinhui/Study/backup'
    # 存放md5值的文件名
    md5file = '/Users/zhonglinhui/Study/backup/md5.data'
    # 设定打包日期
    # %a 获取星期的三位字母缩写
    if time.strftime('%a') == 'Mon':
        full_backup(scr_dir, dst_dir, md5file)
    else:
        incr_backup(scr_dir, dst_dir, md5file)