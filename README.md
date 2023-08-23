# utilbox
python 常用 函数


构建和分发： 

使用 setuptools 等工具来构建和分发您的包。您可以使用 python setup.py sdist 命令来创建一个源代码分发包，或者使用 python setup.py bdist_wheel 命令创建一个可安装的 wheel 包。

发布到 PyPI（可选）：

如果您希望将您的包发布到 Python 包索引（PyPI），您需要注册一个 PyPI 账户，并使用 twine 工具来上传包。运行 twine upload dist/* 命令来上传您的分发包。

pip install git+https://github.com/bit4woo/utilbox.git
