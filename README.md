# 对于python模块的学习

---

[TOC]

## 1.制作Package

### 1.1 \_\_init\_\_.py与\_\_main__.py文件

用简单的话总结：

1. 如果你想把某个文件夹做成一个python包，必须在根目录下添加_\_init\_\_.py文件，空文件也行。在其他程序import时会运行此文件。
2. 如果你想把某个文件夹做成像pip/django/tensorflow那样可以直接通过命令python django运行，必须在根目录下添加_\_main\_\_.py文件。在输入命令python django时会运行此文件。
3. 如果你想把某个文件夹做成python包，并且可以通过命令python -m django以包的形式运行，必须在根目录下添加\_\_init\_\_.py和_\_main\_\_.py文件。在输入命令python -m django时会先运行\_\_init\_\_.py再运行\_\_main\_\_.py

**注意：上面需求2中，因为如果不以包的形式直接运行，搜索模块的路径集将会是当前路径（不会把自身当作包）。因此写\_\_main\_\_.py文件时，如果要import自身的话，要注意搜索模块的路径集，例如pip的\_\_main\_\_.py如下**

```python
import os
import sys

# If we are running from a wheel, add the wheel to sys.path
# This allows the usage python pip-*.whl/pip install pip-*.whl
#此处为判断自身是否以包的形式运行，若__package__ == ''，说明没有把自己识别为包，需要修改搜索模块的路径集。
if __package__ == '':
    # __file__ is pip-*.whl/pip/__main__.py
    # first dirname call strips of '/__main__.py', second strips off '/pip'
    # Resulting path is the name of the wheel itself
    # Add that to sys.path so we can import pip
    path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, path)

#此处引用了自身pip包下的东西
from pip._internal import main as _main  # isort:skip # noqa

if __name__ == '__main__':
    sys.exit(_main())

    
```

**更多参考资料[Package内的\_\_main\_\_.py和\_\_init\_\_.py](<https://blog.csdn.net/ywcpig/article/details/51179547>)**



## 2.打包Package

如果只是想让对方可以import自己做的模块，加入了\_\_init\_\_.py文件其实就已经可以了，下面可以省略不看。

打包的好处在于：

1. 把所有源码转换成两个压缩包的形式传递，方便！
2. 可以用pip安装到虚拟环境，更方便！
3. 甚至可以用官方的代码仓库在线pip install，极其方便！

​	本节参考资料[官网打包入门教程](<https://packaging.python.org/tutorials/packaging-projects/#setup-py>)

### 2.1 创建所需文件

必须创建setup.py文件，LICENSE、README.md根据需求可选填，文件结构如下

```
/python_packaging_learning
  /mypackage
    __init__.py
  setup.py
  LICENSE
  README.md
```

#### 2.1.1 setup.py文件

实例如下

```python
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mypackage-chris633",
    version="1.0.0",
    author="Chris633",
    author_email="chris63388@outlook.com",
    description="My Packaging Note",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Chris633/python_packaging_learning",
    packages=setuptools.find_packages(exclude=['contrib', 'docs', 'tests*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, <4',
    install_requires=['flask>=1.0.0'],
    entry_points={
        'console_scripts': [
            
   		],
	},
)

```

setuptools.setup()的前8个参数显而易见，根据需求填写。几个重要的参数简单介绍，详细内容和关于其余可写参数的内容请看[官网打包及分发详细教程](<https://packaging.python.org/guides/distributing-packages-using-setuptools/#packages>)

--name 打包后的项目名，后缀加自己的名字不是必须的。但这样会解决3.2章节中上传到TestPyPI的一个小问题，这个问题可以先不用考虑，后面会讲。如果你想按照这个教程一步一步走一遍，一定要改变这个参数的值再打包，不要跟我的例子重名

--packages 声明需要打包的内容，可手动填写。但一般用setuptools.find_packages方法自动搜索，并且可以添加exclude来排除不需要打包的内容，如文档文件夹doc。

--classifiers 声明一些内容，如python版本，所用license。此声明只用于在PyPI上的检索，无其他强制作用。

--python_requires 限制python版本

--install_requires 声明能让项目运行的最小依赖集，当项目用pip安装时，会根据依赖集安装相应依赖

--entry_points （貌似是很强大的功能，但还没仔细研究，哪天填坑，[参考资料](<https://packaging.python.org/guides/distributing-packages-using-setuptools/#entry-points>)）

### 2.2 打包命令与本地安装

#### 2.2.1 打包命令

**注意：如果你想用我的例子打包，需要先删除三个文件夹，分别是build，dist，mypackage_chris633.egg-info。**

打包需要先安装两个包setuptools与wheel，命令行或终端下运行下面指令

```
python -m pip install --user --upgrade setuptools wheel
```

之后移动到含有setup.py的根路径下，运行下面的命令，打包

```shell
python setup.py sdist bdist_wheel
```

最后可以看到多了三个文件夹，分别是build，dist，mypackage_chris633.egg-info。

其中dist中的两个压缩文件就是打包好的压缩包。

#### 2.2.2 本地安装

*安装前建议用 [virtualenv](https://packaging.python.org/key_projects/#virtualenv)做好虚拟环境。因为我做的例子里包含了依赖包flask，如果你不介意会在本机环境会安装flask及其依赖，也可不用虚拟环境。*

将dist下的两个压缩文件复制到虚拟环境所在目录下，并在此目录下，运行以下命令

```shell
python -m pip install mypackage_chris633-1.0.1-py3-none-any.whl
```

提示安装成功后，进入python，import mypackage，并进行测试。如下

```powershell
PS C:\Users\chris\Desktop\python_packaging_learning\dist> python -m pip install mypackage_chris633-1.0.1-py3-none-any.whl
Processing c:\users\chris\desktop\python_packaging_learning\dist\mypackage_chris633-1.0.1-py3-none-any.whl
Requirement already satisfied: flask>=1.0.0 in c:\users\chris\appdata\local\programs\python\python37\lib\site-packages (from mypackage-chris633==1.0.1) (1.0.2)
Installing collected packages: mypackage-chris633
Successfully installed mypackage-chris633-1.0.1

PS C:\Users\chris\Desktop\python_packaging_learning\dist> python
Python 3.7.2 (tags/v3.7.2:9a3ffc0492, Dec 23 2018, 23:09:28) [MSC v.1916 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import mypackage
>>> import mypackage.util
>>> mypackage.util.sayhello()
hello
>>>
```



## 3.上传到TestPyPI

做好的包除了可以传递给小伙伴自行本地安装，同时也可以用官方提供仓库TestPyPI。

用了TestPyPI，只需要告诉对方你的包叫啥名，对方就可以直接在线pip install。

### 3.1 准备工作

​	1.去 <https://test.pypi.org/account/register/>注册一个账号

​	2.用如下命令安装twine包。

```shell
python -m pip install --user --upgrade twine
```

### 3.2 上传

用如下命令上传，注意一定要移动至dist的上级目录下

```shell
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

输入这条命令后，会提示你输入你的账户名与密码。上传成功后可以上网查看。

**!!注意:上传到TestPyPI的项目要求不能与他人上传的项目重名。所以可以通过修改在setup.py上的--name参数，以自己的用户名为后缀名即可（官方的建议）。如果你的项目和别人重名则不让上传，并有如下提示**

```shell
> python -m twine upload --repository-url https://test.pypi.org/legac
y/ dist/*
Enter your username: chris633
Enter your password:
Uploading distributions to https://test.pypi.org/legacy/
Uploading mypackage-1.0.0-py3-none-any.whl
100%|█████████████████████████████████████████████████████████ ████████████████████| 5.53k/5.53k [00:03<00:00, 1.60kB/s]
NOTE: Try --verbose to see response content.
HTTPError: 403 Client Error: The user 'chris633' isn't allowed to upload to project 'mypackage'. See https://test.pypi.org/help/#project-name for more information. for url: https://test.pypi.org/legacy/
```

### 3.3 安装

一条指令

```shell
python -m pip install -i https://test.pypi.org/simple/ mypackage-chris633
```

安装后测试同2.2.2中的测试方法