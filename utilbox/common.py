# coding: utf-8
import ipaddress
import logging
import os
import random
import re
import socket
import string
import sys
import urllib
from urllib.parse import urlparse, urlunparse

# 上面是标准库，下面是第三方库库
import socks
# python3.8 -m pip install PySocks
from bs4 import BeautifulSoup


def chose_from_list(items):
    '''
    返回一个选中的list。
    '''
    for index, item in enumerate(items):
        print(f"{index} {item}")
    print(f"{len(items)} all")

    while True:
        try:
            index = int(input("chose your item with index:\n\r"))
            if 0 <= index <= len(items):
                return items[index:index + 1] if index < len(items) else items
            else:
                print("wrong index number")
        except EOFError:
            sys.exit(0)
        except KeyboardInterrupt:
            sys.exit(0)
        except ValueError:
            print("you should input Index Number")


def chose_from_map(items):
    '''
    返回一个选中的list。
    '''
    for index, item in enumerate(items):
        print(f"{index} {item}")
    while True:
        try:
            index = int(input("chose your item with index:\n\r"))
            if 0 <= index <= len(items):
                chosen_key = list(items.keys())[index]
                return items[chosen_key]
            else:
                print("wrong index number")
        except EOFError:
            sys.exit(0)
        except KeyboardInterrupt:
            sys.exit(0)
        except ValueError:
            print("you should input Index Number")


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


def get_file_lines(file_path, spliter=";"):
    encodings_to_try = ['utf-8', 'gbk']  # 尝试的编码列表

    for encoding in encodings_to_try:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                lines = f.readlines()

                if spliter:
                    result = []
                    for line in lines:
                        result.extend(line.split(spliter))
                    return result

                return lines
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    return None  # 如果都尝试失败，则返回 None


def get_lines_from_quote(text, remove_empty_lines=False):
    result = []
    if not text or isinstance(text, str):
        return []
    for item in text.splitlines():
        item = item.strip()
        if remove_empty_lines and item == "":
            continue
        result.append(item)
    return result


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
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(log_file_name)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger = logging.getLogger('main')
    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)
    logger.setLevel(logging.DEBUG)  # 只是将handler的level改成debug是不够的，还需要设置logger本身的level。logger是上游，handler是下游
    logging.basicConfig(
        level=logging.DEBUG)  # https://stackoverflow.com/questions/7016056/python-logging-not-outputting-anything
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


def get_argv(num_of_arg=1):
    result = []
    if len(sys.argv) > num_of_arg:
        # return sys.argv[1:-1] #这是错误的，末尾index所在元素是不会被包含的
        return sys.argv[1:num_of_arg + 222]  # 只要大于长度都可以！
    else:
        index = 0
        while index < num_of_arg:
            arg = input("Enter argument {}: ".format(index + 1))
            result.append(arg)
            index += 1
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


def get_full_path(path):
    if path.startswith("~"):
        path = os.path.expanduser(path)
    if path.startswith("./") or path.startswith(".\\"):
        path = os.path.abspath(path)
    return path


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
    return result_list


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
    return 末尾不包含/
    引用方法:
    from 包名处（模块名称）.文件名称 import 函数名称
    包或者模块，是指含有__init__.py的文件夹
    """
    parsed_url = urlparse(url)
    base_url = urlunparse((parsed_url.scheme, parsed_url.netloc, '', '', '', ''))
    return base_url


def read_lines_from_console(clear_empty=False, strip_lines=False):
    lines = []

    print("Enter multiple lines of text (Ctrl+D or Ctrl+Z to end):")
    while True:
        try:
            line = input()
            if strip_lines:
                line = line.strip()
            if not clear_empty or line:
                lines.append(line)
        except EOFError:
            break

    return lines


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


if __name__ == '__main__':
    # print(is_valid_subnet("192.168.15.0/25"))
    # print(get_ip_list_of_subnet("192.168.15.0/25"))
    print(get_ip("baidu.com"))
