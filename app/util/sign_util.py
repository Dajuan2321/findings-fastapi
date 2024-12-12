import hashlib
import random
import string


def sha256_hash(data: str) -> str:
    # 创建一个新的 SHA-256 哈希对象
    sha256 = hashlib.sha256()

    # 更新哈希对象以包含要哈希的数据，注意需要将字符串编码为字节
    sha256.update(data.encode('utf-8'))

    # 获取哈希值的十六进制表示
    hex_digest = sha256.hexdigest()

    return hex_digest

def generate_random_string(length):
    # 定义可用字符集：所有大小写字母加上数字
    characters = string.ascii_letters + string.digits

    # 从字符集中随机选择指定数量的字符，并组成一个字符串
    random_string = ''.join(random.choice(characters) for i in range(length))

    return random_string