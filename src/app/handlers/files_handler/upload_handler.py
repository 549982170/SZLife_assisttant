# coding:utf-8
# !/user/bin/python
'''
Created on 2017年9月11日
@author: yizhiwu
文件上传handler
'''
import os
import uuid

from app.handlers.base_handler import Component
from app.share.constants import ALLOWED_EXTENPICSIONS, COMPRESSIONPICTURE
from app.share.exceptions import ApiException
from app.share.util import get_today_date, getUploadFilePath, \
    mysecure_filename, is_picture, compressPic


class Upload(Component):
    '''文件上传'''

    def __init__(self, owner):
        Component.__init__(self, owner)

    def uploadPic(self, imgdata, filePath):
        """上传图片"""
        filename = mysecure_filename(imgdata.filename)
        extension = os.path.splitext(filename)[1].lower()  # 文件拓展名

        if not is_picture(imgdata):
            return None
        dateStr = get_today_date()  # 日期
        folder = os.path.join(filePath, dateStr)  # 上传文件保存路径
        uuidfilename = str(uuid.uuid1()) + extension  # 随机文件
        filepath = os.path.join(getUploadFilePath(folder), uuidfilename).replace("\\", "/")
        imgdata.save(filepath)
        return filepath

    def uploadPicPathList(self, imgdata, filePath_list):
        """多层路径上传图片"""
        filename = mysecure_filename(imgdata.filename)
        extension = os.path.splitext(filename)[1].lower()  # 文件拓展名
        if not is_picture(imgdata):
            return None
        dateStr = get_today_date()  # 日期
        filePath_list.append(dateStr)
        folder = os.sep.join(filePath_list)  # 上传文件保存路径
        uuidfilename = str(uuid.uuid1()) + extension  # 随机文件
        filepath = os.path.join(getUploadFilePath(folder), uuidfilename).replace("\\", "/")
        imgdata.save(filepath)
        return filepath, filename

    def uploadFiles(self, files, filePath_list, allow_type_list=None):
        """上传文件
        @param allow_type_list: 允许上传的文件名后缀
        @param filePath_list:  多层目录列表"""
        filename = mysecure_filename(files.filename)
        extension = os.path.splitext(filename)[1].lower()  # 文件拓展名
        if allow_type_list and extension not in allow_type_list:
            raise ApiException(msg=u"上传的文件格式有误")
        dateStr = get_today_date()  # 日期
        filePath_list.append(dateStr)
        folder = os.sep.join(filePath_list)  # 上传文件保存路径
        uuidfilename = str(uuid.uuid1()) + extension  # 随机文件
        filepath = os.path.join(getUploadFilePath(folder), uuidfilename).replace("\\", "/")
        files.save(filepath)
        return filepath, filename

    def compressFiles(self, files_path):
        """压缩文件"""
        extension = os.path.splitext(files_path)[1].lower()  # 文件拓展名
        if extension in ALLOWED_EXTENPICSIONS:  # 图片
            compress_path = compressPic(files_path, addname=COMPRESSIONPICTURE)
        else:
            compress_path = files_path
        return compress_path

