#!/usr/bin/python
##by linxiaobai@live.com
##install GraphicsMagick and config related env
# -*- coding: utf-8 -*-
import os
import codecs
import time
from multiprocessing import cpu_count

env_file_path = "/etc/profile"
#softs order can't be modify  libjepg-turbo need nasm, libpng need zlib
softs = ("nasm-2.12.02", "zlib-1.2.11", "libjpeg-turbo-1.5.1", "libpng-1.6.28", "libwebp-0.5.0", "tiff-4.0.4", "GraphicsMagick-1.3.25")
suffix = ".tar.gz"
root_path = "/opt/"
base_path = root_path + "softs/"

class RunShellError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		repr(self.value)


def run_shell(command):
	ret = os.system(command)
	if (ret != 0):
		raise RunShellError("run `" + command + "` failed, ret:" +  str(ret))
	print "`" + command + "` exec success"
	time.sleep(2)

def change_dir(new_dir):
	current_path = os.getcwd()
	print "current path:" + current_path
	print "change dir to " + new_dir
	os.chdir(new_dir)
	current_path = os.getcwd()
	print "current path:" + current_path
	time.sleep(2)

def unpack_all():
	#run_shell("sudo su - ") ##get root auth
	change_dir(base_path)
	for tar in softs:
		unpack_one(tar + suffix)

def unpack_one(pack_file):
	print "###start unpackaging " + pack_file + "###"
	package = base_path + pack_file
	os.system("tar xvf " + package);
	print "###unpackage " + pack_file + "end###"

def get_install_dir(soft_dir):
	idx = soft_dir.rfind("-")
	install_dir = root_path + soft_dir[0:idx]
	return install_dir

def check_is_config_path(path):
	f = codecs.open(env_file_path, 'r')
	data = f.readlines()
	start_idx = 0 - len(data);
	for i in xrange(start_idx, 0):
		line = data[i].strip().lower()
		if (line.find("export") >= 0 and line.find(path.lower()) >= 0):
			return True
	return False
#has a bug, can't let env work in shell
def config_sys_path(path):
	if (check_is_config_path(path)):
		print path + " has already been config"
		return
	f = codecs.open(env_file_path, 'a') #'a' means append to the original file
	env_path = "export PATH=$PATH:" + path
	f.write("\n" + env_path)
	if (path.find("GraphicsMagick") >= 0):
		cpu_num = cpu_count()
		f.write("\nexport OMP_NUM_THREADS=" + str(cpu_num))
	f.close()
	run_shell("source " + env_file_path)

def handler_zlib(zlib_name):
	idx = zlib_name.rfind("-") + 1
	zlib_verson = zlib_name[idx:]
	run_shell("cp /usr/local/lib/libz.so." + zlib_verson + " /lib64/")
	change_dir("/lib64/")
	run_shell("rm -rf libz.so.1")
	run_shell("ln -s libz.so." + zlib_verson + " libz.so.1")

def install_all():
	for s in softs:
		change_dir(base_path + s)
		install_dir = get_install_dir(s)
		if (s.find("zlib") >= 0):
			run_shell("./configure")
		elif (s.find("GraphicsMagick") >= 0):
			run_shell("./configure  '--prefix=" + install_dir + "' '-enable-openmp' '-enable-shared' 'CPPFLAGS=-I/opt/libjpeg-turbo/include/ -I/opt/libpng/include/ -I/opt/tiff/include/ -I/opt/libwebp/include/' 'LDFLAGS=-L/opt/libjpeg-turbo/lib64/ -L/opt/libpng/lib/ -L/opt/tiff/lib/ -L/opt/libwebp/lib/'")
		else:
			run_shell("./configure --prefix=" + install_dir)
		run_shell("make")
		run_shell("make install")
		if (s.find("nasm") >= 0 or s.find("GraphicsMagick") >= 0):
			config_sys_path(install_dir + "/bin")
		if (s.find("zlib") >= 0):
			handler_zlib(s)

if __name__=='__main__':
	print "###start unpack all###"
	unpack_all()
	print "###unpack all end###"
	print "###start install all###"
	install_all()
	print "###install all end###"

