# utilbox
我的python常用函数合集，为了方便在多个项目间共享，创建了这个项目。

python环境：python3.8

由于可能经常更新这个包package，而不想维护版本，每次更新都需要重新安装到自己的环境中。



## 安装方法

```
python3.8 -m pip install -I git+https://github.com/bit4woo/utilbox.git

或

python3.8 -m pip uninstall utilbox
python3.8 -m pip install git+https://github.com/bit4woo/utilbox.git
```



## 使用方法

```
import utils

utils.get_base_url("https://github.com/bit4woo/utilbox.git")

import

```





## 如何强制重新安装?即使版本没有变化

由于可能经常更新这个包package，而不想维护版本，每次更新都需要重新安装到自己的环境中。参考以下方法：



1. **卸载后重新安装（推荐）：** 首先，卸载当前已安装的包，然后再重新安装它。您可以使用以下命令：

   ```bash
   python3.8 -m pip uninstall utilbox
   
   python3.8 -m pip install git+https://github.com/bit4woo/utilbox.git
   ```
   
2. **使用 `--upgrade` 参数（没用！！！）：** 使用 `--upgrade` 参数可以让 `pip` 在安装包时忽略已安装版本，强制安装最新版本。即使包的版本号没有变化，它也会重新下载并安装。使用以下命令：

   ```bash
   python3.8 -m pip install --upgrade git+https://github.com/bit4woo/utilbox.git
   ```

   

3. **使用 `-I` 参数（可用，不推荐）：** 在一些情况下，您可能需要使用 `-I` 参数来强制安装，即使包已经在环境中存在。使用以下命令：

   ```bash
   python3.8 -m pip install -I git+https://github.com/bit4woo/utilbox.git
   ```

   

## setup.py的配置

setup的基本逻辑就是复制指定的目录或者文件到python环境相应的目录中。

如果package项目中，目录名称修改了，在使用这个package时，import xxx的名称也需要改！！！所以最好固定这个名称！！！



对于影响源码文件复制的参数：

- `packages` 和 `py_modules`：这两个参数指定了哪些源码文件将被复制和安装。`packages` 列出了包含子包和模块的目录，`py_modules` 列出了单个模块文件。
- `scripts`：这个参数指定要安装为脚本的文件路径，这些文件将被复制到系统的可执行路径下。

```
packages： 列出要包含在包中的子包和模块。这将影响哪些源码文件会被复制和安装。 
py_modules： 列出要包含在包中的单个模块文件。这将影响哪些单个模块文件会被复制和安装。
```

## packge中源码目录变更对比测试

pip 从github 安装时，使用指定的commit：

```
python3.8 -m pip install -I git+https://github.com/bit4woo/utilbox.git@babdb2ecdbdd636ecf81c93805a5f443f2ba0215
```

![image-20230823150453623](assets/image-20230823150453623.png)

#### 1、源码目录是utilbox

![image-20230823144846848](assets/image-20230823144846848.png)

#### 2、源码目录是utils

![image-20230823145604639](assets/image-20230823145604639.png)

#### 3、函数调用的变化

![image-20230823145950951](assets/image-20230823145950951.png)



## 强制更新命令对比测试

#### 1、--upgrade可以弃用了

![image-20230823151327167](assets/image-20230823151327167.png)

#### 2、-I参数可以使用，但是存流程垃圾文件，容易造成混淆困扰，也不建议使用

![image-20230823151515961](assets/image-20230823151515961.png)

#### 3、最好还是先卸载再安装！

![image-20230823152050323](assets/image-20230823152050323.png)

#### 4、目录不变，源码变化

```
当目录没有变化，源码变化时进行了测试，--upgrade没有更新源码，-I成功更新了源码
```



## python setup.py install

```
python setup.py install --force
--force 参数，该参数可以强制覆盖已安装的包
```

当在项目目录中执行以上命令时，它没有将源码文件复制到 [site-packages](C:\Python382\Lib\site-packages) 中，而是生成了一个utilbox-0.1.0-py3.8.egg文件

![image-20230823143203605](assets/image-20230823143203605.png)
