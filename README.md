# utilbox
我的python常用函数合集，为了方便在多个项目间共享，创建了这个项目。

python环境：python3.8

由于可能经常更新这个包package，而不想维护版本，每次更新都需要重新安装到自己的环境中。



## 安装方法

```
python3.8 -m pip install --upgrade git+https://github.com/bit4woo/utilbox.git
```



## 如何强制重新安装?即使版本没有变化

由于可能经常更新这个包package，而不想维护版本，每次更新都需要重新安装到自己的环境中。参考以下方法：



1. **卸载后重新安装：** 首先，卸载当前已安装的包，然后再重新安装它。您可以使用以下命令：

   ```bash
   python3.8 -m pip uninstall utilbox
   
   python3.8 -m pip install git+https://github.com/bit4woo/utilbox.git
   ```
   
2. **使用 `--upgrade` 参数：** 使用 `--upgrade` 参数可以让 `pip` 在安装包时忽略已安装版本，强制安装最新版本。即使包的版本号没有变化，它也会重新下载并安装。使用以下命令：

   ```bash
   python3.8 -m pip install --upgrade git+https://github.com/bit4woo/utilbox.git
   ```

   

3. **使用 `-I` 参数：** 在一些情况下，您可能需要使用 `-I` 参数来强制安装，即使包已经在环境中存在。使用以下命令：

   ```bash
   python3.8 -m pip install -I git+https://github.com/bit4woo/utilbox.git
   ```

   

