# GraphicsMagickInstallShell
安装GraphicsMagick脚本



脚本里配置环境变量是无法生效的
详见:https://www.zhihu.com/question/55937152

config_sys_path里source无效，最终还需要手动在终端source /etc/profile
只能先执行环境变量配置了
```
export PATH=$PATH:/opt/nasm/bin
export PATH=$PATH:/opt/GraphicsMagick/bin
export OMP_NUM_THREADS=24
```
