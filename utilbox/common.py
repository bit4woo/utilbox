# coding: utf-8
import base64
import binascii
import datetime
import hashlib
import ipaddress
import logging
import os
import random
import re
import socket
import string
import subprocess
import sys
import urllib
from collections import OrderedDict
from urllib.parse import urlparse, urlunparse

# 上面是标准库，下面是第三方库库
import socks
# python3.8 -m pip install PySocks
from bs4 import BeautifulSoup, Tag


def choose_from_list(items):
    """
    返回一个选中的list。
    """
    while True:
        try:
            print("Available options:")
            for index, item in enumerate(items):
                print(f"{index} {item}")
            print(f"{len(items)} all")

            user_input = input("Choose your item(s) with index (comma-separated for multiple):\n")

            if user_input.lower() == 'all':
                return items

            selected_indices = [int(index.strip()) for index in user_input.split(',') if index.strip().isdigit()]

            if all(0 <= index < len(items) for index in selected_indices):
                return [items[index] for index in selected_indices]
            else:
                print("Invalid index number. Please try again.")

        except EOFError:
            sys.exit(0)
        except KeyboardInterrupt:
            sys.exit(0)
        except ValueError:
            print("Invalid input. Please enter valid index number(s).")


def choose_from_iterable(iterable):
    """
    返回一个选中的list。
    """
    ordered_iterable = iterable

    # 如果输入是字典，则转换为有序字典
    if isinstance(iterable, dict):
        ordered_iterable = OrderedDict(iterable)

    while True:
        try:
            print("Available options:")
            for index, item in enumerate(ordered_iterable):
                print(f"{index} {item}")
            print(f"{len(ordered_iterable)} all")

            user_input = input("Choose your item(s) with index (comma-separated for multiple):\n")

            if user_input.lower() == 'all':
                return list(ordered_iterable.values())

            selected_indices = [int(index.strip()) for index in user_input.split(',') if index.strip().isdigit()]

            if all(0 <= index < len(ordered_iterable) for index in selected_indices):
                selected_items = [list(ordered_iterable.values())[index] for index in selected_indices]
                return selected_items
            else:
                print("Invalid index number. Please try again.")

        except EOFError:
            sys.exit(0)
        except KeyboardInterrupt:
            sys.exit(0)
        except ValueError:
            print("Invalid input. Please enter valid index number(s).")


def get_file_content(file_path):
    encodings = ["utf-8", "gbk"]
    for encoding in encodings:
        try:
            with open(file_path, "r", encoding=encoding) as fp:
                return fp.read()
        except:
            continue
    return None


def get_full_path(path):
    if path.startswith("~"):
        path = os.path.expanduser(path)
    if path.startswith("./") or path.startswith(".\\"):
        path = os.path.abspath(path)
    return path


def clean_list(lines, spliter=None, do_strip=True, remove_empty=True):
    """
    如果有分割符，会对每行再进行分割
    默认对每个元素进行strip
    默认删除空字符串
    :param lines:
    :param spliter:
    :param do_strip:
    :param remove_empty:
    :return:
    """
    if isinstance(lines, list):
        if spliter:
            lines = [item for line in lines for item in line.split(spliter)]
        if do_strip:
            lines = [line.strip() for line in lines]
        if remove_empty and "" in lines:
            lines = [line for line in lines if line != ""]
        return lines
    return lines


def get_lines_from_file(file_path, spliter=";", do_strip=True, remove_empty=True):
    """
    从文件中读行，返回一个列表。
    如果有分割符，会对每行再进行分割
    默认对每个元素进行strip
    默认删除空字符串
    :param file_path:
    :param spliter:
    :param do_strip:
    :param remove_empty:
    :return:
    """
    encodings_to_try = ['utf-8', 'gbk']  # 尝试的编码列表

    for encoding in encodings_to_try:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                lines = f.readlines()
                return clean_list(lines, spliter, do_strip, remove_empty)
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    return None  # 如果都尝试失败，则返回 None


def get_lines_from_quote(text, spliter=";", do_strip=True, remove_empty=True):
    if not text or not isinstance(text, str):
        return []

    lines = text.splitlines()
    return clean_list(lines, spliter, do_strip, remove_empty)


def get_lines_from_console(spliter=";", do_strip=True, remove_empty=True):
    lines = []

    print("Enter multiple lines of text (Ctrl+D or Ctrl+Z to end):")
    while True:
        try:
            line = input()
            lines.append(line)
        except EOFError:
            break

    return clean_list(lines, spliter, do_strip, remove_empty)


def is_valid_domain(domain):
    domain_pattern = "^((?!-)[A-Za-z0-9-]{1,63}(?<!-)\\.)+[A-Za-z]{2,6}$"
    return re.match(domain_pattern, domain) is not None


def is_valid_host(host):
    if not host:
        return False
    try:
        return is_valid_domain(host) or is_valid_ip(host)
    except:
        return False


def is_valid_ip(host):
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def is_valid_subnet(subnet):
    '''
    strict =False，因为想要 192.168.1.1/27这个格式返回true
    :param subnet:
    :return:
    '''
    try:
        ipaddress.ip_network(subnet, strict=False)
        return True
    except ValueError:
        return False


def is_valid_domain_by_query(host):
    try:
        socket.getaddrinfo(host, None)
        return True
    except socket.gaierror:
        return False


def is_valid_port(port):
    try:
        p = int(port)
        if 0 <= p <= 65535:
            return True
    except:
        pass
    return False


def get_ip_list_of_subnet(subnet):
    try:
        tmp = ipaddress.ip_network(subnet, strict=False)
        result = [item.__str__() for item in tmp.hosts()]
        return result
    except ValueError:
        return []


def get_logger(log_file_name='logger.log'):
    """
    # https://stackoverflow.com/questions/7016056/python-logging-not-outputting-anything
    # 只是将handler的level改成debug是不够的，还需要设置logger本身的level。logger是上游，handler是下游
    :param log_file_name:
    :return:
    """
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    # 使用basicConfig设置全局的日志级别
    logging.basicConfig(level=logging.DEBUG)

    # 创建logger
    logger = logging.getLogger('main')

    # 创建和设置StreamHandler和FileHandler
    handlers = [logging.StreamHandler(sys.stdout), logging.FileHandler(log_file_name, encoding="utf-8")]
    for handler in handlers:
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def gen_random_str(to_void):
    # 定义包含所有可能字符的字符集合
    while True:
        # characters = string.ascii_letters + string.digits + string.punctuation
        characters = string.ascii_letters + string.digits
        # 使用random.choices()函数从字符集合中随机选择字符，并生成随机字符串
        random_string = ''.join(random.choices(characters, k=5))

        if to_void and random_string in to_void:
            continue
        else:
            return random_string


def highlight_print(content, tips=""):
    if not tips:
        tips = ""
    print()
    print(("#" * 10 + "{}" + "#" * 10).format(tips))
    print(content)
    print("#" * (20 + len(str(tips))))
    print()


def set_socks_proxy(proxy_host, proxy_port):
    """
    设置全局的 SOCKS 代理，适用于所有套接字操作。
    socks.set_default_proxy()  # 取消代理设置
    """
    try:
        import socks
        import socket
        proxy_port = int(proxy_port)
        print("set proxy: {}:{}".format(proxy_host, proxy_port))
        socks.set_default_proxy(socks.SOCKS5, proxy_host, proxy_port)
        socket.socket = socks.socksocket
        return True
    except:
        print("set socks proxy failed!!!")
        return False


def is_using_socks_proxy():
    """
    检测当前程序是否使用了 SOCKS 代理。

    :return: 如果使用了 SOCKS 代理，返回 True；否则返回 False。
    """

    import socket
    return socket.socket == socks.socksocket


def get_base_url(url):
    '''
    return 末尾不包含/
    引用方法:
    from 包名处（模块名称）.文件名称 import 函数名称
    包或者模块，是指含有__init__.py的文件夹
    '''
    parsed_url = urlparse(url)
    base_url = urlunparse((parsed_url.scheme, parsed_url.netloc, '', '', '', ''))
    return base_url


def url_encode(url):
    return urllib.parse.quote(url)


def url_decode(url):
    return urllib.parse.unquote(url)


def get_input_values(*arg_name):
    """
    从用户输入获取多个变量的值，类似如下的用法
    get_input_values("param1", "param2", "param3")
    :param arg_name:
    :return: 返回参数名和值的字典
    """
    result = dict()  # 还是用dict类型，结果不容易出错
    # 运行程序时，有参数传递，那么就直接使用
    if len(sys.argv) > len(arg_name):
        for i, arg in enumerate(arg_name):
            result[arg] = sys.argv[i + 1]
    else:  # 没有参数传递，要求用户输入
        for arg in arg_name:
            if arg is None or not isinstance(arg, str):
                continue
            arg_value = input(f"Enter [{arg}] value: ")
            result[arg] = arg_value
    return result


def get_textarea_contents(html, name=None):
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    if name:
        # Find all <textarea> tags with the specified name attribute and extract their content
        textarea_contents = [textarea.text.strip() for textarea in soup.select(f'textarea[name="{name}"]')]
    else:
        # Find all <textarea> tags and extract their content
        textarea_contents = [textarea.text.strip() for textarea in soup.find_all('textarea')]

    return textarea_contents


def get_content_by_class(html, class_name):
    """
    根据
    :param html:
    :param class_name:
    :return:
    """
    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(html, 'html.parser')

    # 使用 CSS 选择器定位元素
    elements = soup.select(f'.{class_name}')

    # 提取元素的内容
    content = [element.get_text() for element in elements]

    return content


def get_content_by_element(html, element_name):
    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(html, 'html.parser')

    # 使用 CSS 选择器定位元素
    elements = soup.select(element_name)

    # 提取元素的内容
    content = [element.get_text() for element in elements]

    return content


def get_element_text(element):
    """
    获取BeautifulSoup的Tag对象，也就是HTML元素的文本内外，比如textarea中的字符串
    :param element:
    :return:
    """
    if isinstance(element, Tag):
        return element.get_text()
    elif hasattr(element, '__iter__'):
        result = []
        for item in element:
            result.append(get_element_text(item))
        return result


def get_element_attr(element, attr_name):
    """
    获取BeautifulSoup的Tag对象，也就是HTML元素的属性值
    :param element:
    :param attr_name:
    :return:
    """
    if isinstance(element, Tag):
        return element.get(str(attr_name).lower())
    elif hasattr(element, '__iter__'):
        result = []
        for item in element:
            result.append(get_element_attr(item, attr_name))
        return result


def find_elements(html, name, attr_names: list = None, keywords: list = None):
    """
    HTML元素指的是从开始标签（start tag）到结束标签（end tag）的所有代码。BeautifulSoup的Tag对象（即元素）
    元素可拥有属性，属性总是以名称/值对的形式出现，比如：name="value"。
    class、id等是大多数HTML元素都有的属性
    <input checkDependsOn="credentialsId" checkMethod="post" checkUrl="/job/" name="_.url" placeholder="" type="text" class="jenkins-input validated  " value="">
    :param html:
    :param keywords: 关键词列表，将整个元素当作字符串看待，字符串需要包含所有的关键词
    :param attr_names: 传递一个列表，列表中的元素是需要包含的属性名称
    :param name: 的作用对象是tag的名称，比如input、head等
    :return Tag对象的list
    """
    if keywords is None:
        keywords = []
    if attr_names is None:
        attr_names = []
    result = []
    soup = BeautifulSoup(html, 'html.parser')

    result_dict = {str(attr_name).lower(): True for attr_name in attr_names if str(attr_name).lower() not in ["name"]}
    # 需要排除和find_all同名的参数，否则会报错
    # 使用字典解包的方式将值传递给函数作为参数
    elements = soup.find_all(name=name, **result_dict)

    # 使用集合来加速关键词匹配
    keywords_set = set(keywords)
    for element in elements:
        # 将元素转换为字符串，然后检查关键词是否在其中
        element_str = str(element)
        if all(keyword in element_str for keyword in keywords_set):
            result.append(element)
    return result


def get_full_path(path):
    if path.startswith("~"):
        path = os.path.expanduser(path)
    if path.startswith("./") or path.startswith(".\\"):
        path = os.path.abspath(path)
    return path


def is_file_path_by_pattern(path):
    # 定义常见文件路径的正则表达式模式
    path_patterns = [
        r'^[a-zA-Z]:\\[^:*?"<>|\r\n]*$',  # Windows 绝对路径
        r'^[a-zA-Z]:/[^:*?"<>|\r\n]*$',  # Windows 绝对路径（斜杠）
        r'^/[^:*?"<>|\r\n]*$',  # Linux/MacOS 绝对路径
        r'^\.[a-zA-Z0-9_/-]*$',  # 相对路径
        r'^\.\.[a-zA-Z0-9_/-]*$'  # 相对路径（上级目录）
    ]

    # 使用正则表达式匹配路径
    for pattern in path_patterns:
        if re.match(pattern, path):
            return True

    # 如果没有匹配任何模式，则判定为无效路径
    return False


def get_ip(host):
    try:
        return socket.gethostbyname(host)
    except:
        return None


def startswith_regex(pattern, text):
    """
    尝试从字符串的[开头]匹配模式，如果匹配成功则返回True，否则返回False
    """
    match = re.match(pattern, text)
    if match:
        return True
    else:
        return False


def extract_between(text, start, end):
    """
    提取2个字符串之间的内容,返回一个列表
    :param text:
    :param start:
    :param end:
    :return:
    """
    pattern = re.escape(start) + r"(.*?)" + re.escape(end)
    matches = re.findall(pattern, text)
    if matches:
        return matches
    else:
        return []


def findfirst_regex(pattern, text):
    """
    在整个字符串中搜索匹配，如果找到则返回一个匹配对象，否则返回None
    """
    if not (pattern and text):
        return None
    search_result = re.search(pattern, text)
    if search_result:
        return search_result.group(0)
    return None


# 使用re.findall查找所有匹配
def findall_regex(pattern, text):
    """
    <td><a href="(.*?)" class="model-link inside">
    根据正则表达式提取所有匹配的内容，返回一个列表
    """
    if not (pattern and text):
        return []
    result_list = re.findall(pattern, text)
    return result_list or []  # 如果result_list为空，则返回一个空列表


def replaceall_regex(pattern, replaceto, text):
    """
    将正则表达式匹配到的内容替换为replaceto的内容，返回替换后的完整文本
    """
    if not (pattern and replaceto and text):
        return text
    new_text = re.sub(pattern, replaceto, text)
    return new_text


def get_base_url(url):
    """
    return 末尾不包含/，类似http请求的Origin header
    Origin: https://www.example.com
    Referer: https://www.example.com/user/login
    引用方法:
    from 包名处（模块名称）.文件名称 import 函数名称
    包或者模块，是指含有__init__.py的文件夹
    """
    parsed_url = urlparse(url)
    base_url = urlunparse((parsed_url.scheme, parsed_url.netloc, '', '', '', ''))
    return base_url


def get_files_in_path(path):
    """
    获取某个路径中所有文件的绝对路径
    """
    file_list = []

    # 如果是文件，直接返回文件的绝对路径
    if os.path.isfile(path):
        return [os.path.abspath(path)]

    # 如果是目录，遍历目录及其子目录，返回所有文件的绝对路径列表
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                file_list.append(os.path.abspath(file_path))

    return file_list


def contains_any(string, keywords):
    """
    判断string是否包含任何一个关键词
    """
    if isinstance(keywords, str):
        return keywords in string
    if isinstance(keywords, (list, set)):
        for keyword in keywords:
            if keyword in string:
                return True
    return False


def print_all_str_vars(keywords_to_exclude=None):
    """
    打印用户定义的所有字符串变量，可以设置关键词根据变量名进行排除
    """
    if keywords_to_exclude is None:
        keywords_to_exclude = {}
    all_variables = globals()

    for var_name, var_value in all_variables.items():
        if not isinstance(var_value, str):
            continue
        if var_name.startswith("__") and var_name.endswith("__"):
            continue
        if contains_any(var_name, keywords_to_exclude):
            continue
        else:
            print(var_value)


def split_line(line):
    """
    将一行字符串分割成多个部分，连续的tab和空格都当作一个分隔符
    testcase = "This\tis   \t  a\t\t  test 	  string\t"
    testcase = "aaa	bbb"
    :param line:
    :return:
    """
    # parts = re.split(r'\s+|\t+', line)
    parts = line.split()
    # 字符串的split函数本身就有这样的能力
    return parts


def md5(input_string):
    # 创建一个 MD5 哈希对象
    md5_hash = hashlib.md5()

    # 更新哈希对象以包含输入字符串的字节表示
    md5_hash.update(input_string.encode('utf-8'))

    # 获取 MD5 哈希值的十六进制表示
    md5_hex = md5_hash.hexdigest()

    return md5_hex


def get_time_str():
    """
    返回当前时间的字符串，常用于文件名
    :return:
    """
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y_%m_%d_%H_%M_%S_%f")[:-3]
    return formatted_time


def run_external_program(command):
    """
    注意，要执行的命令、脚本，基本都要求绝对路径
    :param command:
    :return:
    """
    try:
        # Run the external program and capture its output
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

        # Check if the command was successful (return code 0)
        if result.returncode == 0:
            # Return the standard output
            return result.stdout.strip()
        else:
            # If the command failed, print the error message
            print(f"Error: {result.stderr.strip()}")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def deduplicate_list(input_list):
    # 使用OrderedDict.fromkeys()去重，并保持原始顺序
    deduplicated_dict = OrderedDict.fromkeys(input_list)

    # 将字典的键转换回列表
    deduplicated_list = list(deduplicated_dict.keys())

    return deduplicated_list


def is_hex_code(input_str):
    """
    hello -- 68656C6C6F
    :param input_str:
    :return:
    """
    return re.match(r"^[0-9a-fA-F]+$", input_str) is not None


def hex_code_to_byte_array(hex_code):
    r"""
    68656C6C6F --- b'hello'
    1112136162 --- b'\x11\x12\x13ab'
    可以打印的字符直接以字符表示，不行的用\x加code
    :param hex_code:
    :return:
    """
    return bytes.fromhex(hex_code)


def byte_array_to_hex_code(byte_array):
    """
    使用方法
    byte_array_to_hex_code(b"hello") -- bytes can only contain ASCII literal characters.
    byte_array_to_hex_code("hello中文".encode())
    :param byte_array:
    :return:
    """
    # 使用 binascii.hexlify 将字节数组转换为 hex code
    hex_code = binascii.hexlify(byte_array).decode()
    return hex_code


def is_base64(input_str):
    try:
        base64.b64decode(input_str)
        return True
    except ValueError:
        return False


def base64_encode(data):
    """
    传入的参数可以是 str 或者 byte array格式
    encode --- str to byte array
    decode --- byte array to str
    :param data:
    :return:
    """
    if isinstance(data, str):
        data = data.encode()

    # 进行 Base64 编码
    encoded_data = base64.b64encode(data).decode()
    return encoded_data


def base64_decode(data):
    """
    解码后，如果转化为字符串就返回字符串，否则就返回byte[]
    :param data:
    :return:
    """
    # 尝试解码成字符串
    try:
        decoded_str = base64.b64decode(data).decode()
        return decoded_str
    except UnicodeDecodeError:
        # 解码成字符串失败，返回字节数组
        decoded_bytes = base64.b64decode(data)
        return decoded_bytes
    except Exception:
        return None


def get_files_in_dir(directory, extensions=None, include_subdir=True):
    """
    获取目录下的所有文件。

    参数：
    - directory: 目标目录的路径。
    - extensions: 文件后缀过滤列表，例如 ['.txt', '.pdf']，默认为 None。
    - include_subdir: 是否遍历子目录，True 为遍历，False 为不遍历，默认为 True。

    返回：
    包含所有文件路径的列表。
    """
    files = []

    extensions = tuple(extensions) if extensions else None

    def is_valid_file(filename):
        return extensions is None or filename.endswith(extensions)

    if include_subdir:
        # 遍历目录及其子目录
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                if is_valid_file(filename):
                    files.append(os.path.join(root, filename))
    else:
        # 不遍历子目录，直接获取目录下的文件列表
        files = [os.path.join(directory, filename) for filename in os.listdir(directory)
                 if os.path.isfile(os.path.join(directory, filename)) and is_valid_file(filename)]

    return files


if __name__ == '__main__':
    param1 = get_input_values("url")
    print(param1)
