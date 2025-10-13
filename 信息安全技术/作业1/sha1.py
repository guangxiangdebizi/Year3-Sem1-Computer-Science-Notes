"""
SHA-1 (Secure Hash Algorithm 1) 算法手动实现
不使用任何第三方加密库，从底层实现SHA-1算法
"""


class SHA1:
    """SHA-1哈希算法实现类"""
    
    def __init__(self):
        """初始化SHA-1对象"""
        # 初始哈希值 (5个32位字)
        self.h0 = 0x67452301
        self.h1 = 0xEFCDAB89
        self.h2 = 0x98BADCFE
        self.h3 = 0x10325476
        self.h4 = 0xC3D2E1F0
    
    def _left_rotate(self, n, b):
        """
        32位整数循环左移
        :param n: 要移位的数
        :param b: 移位位数
        :return: 移位后的结果
        """
        return ((n << b) | (n >> (32 - b))) & 0xffffffff
    
    def _pad_message(self, message):
        """
        对消息进行填充
        :param message: 原始消息字节串
        :return: 填充后的消息
        """
        msg_len = len(message)
        message += b'\x80'
        
        # 填充0，使得消息长度 ≡ 448 (mod 512)
        while len(message) % 64 != 56:
            message += b'\x00'
        
        # 添加原始消息长度（以位为单位，64位大端序）
        message += (msg_len * 8).to_bytes(8, byteorder='big')
        
        return message
    
    def _process_chunk(self, chunk):
        """
        处理一个512位的消息块
        :param chunk: 512位(64字节)的消息块
        """
        # 将块分成16个32位的字
        w = []
        for i in range(0, 64, 4):
            w.append(int.from_bytes(chunk[i:i+4], byteorder='big'))
        
        # 扩展为80个字
        for i in range(16, 80):
            w.append(self._left_rotate(w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16], 1))
        
        # 初始化工作变量
        a = self.h0
        b = self.h1
        c = self.h2
        d = self.h3
        e = self.h4
        
        # 主循环
        for i in range(80):
            if 0 <= i <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else:  # 60 <= i <= 79
                f = b ^ c ^ d
                k = 0xCA62C1D6
            
            temp = (self._left_rotate(a, 5) + f + e + k + w[i]) & 0xffffffff
            e = d
            d = c
            c = self._left_rotate(b, 30)
            b = a
            a = temp
        
        # 更新哈希值
        self.h0 = (self.h0 + a) & 0xffffffff
        self.h1 = (self.h1 + b) & 0xffffffff
        self.h2 = (self.h2 + c) & 0xffffffff
        self.h3 = (self.h3 + d) & 0xffffffff
        self.h4 = (self.h4 + e) & 0xffffffff
    
    def hash(self, message):
        """
        计算消息的SHA-1哈希值
        :param message: 输入消息（字符串或字节串）
        :return: 160位哈希值（十六进制字符串）
        """
        # 重置哈希值
        self.h0 = 0x67452301
        self.h1 = 0xEFCDAB89
        self.h2 = 0x98BADCFE
        self.h3 = 0x10325476
        self.h4 = 0xC3D2E1F0
        
        # 将字符串转换为字节
        if isinstance(message, str):
            message = message.encode('utf-8')
        
        # 填充消息
        padded_message = self._pad_message(message)
        
        # 处理每个512位块
        for i in range(0, len(padded_message), 64):
            self._process_chunk(padded_message[i:i+64])
        
        # 生成最终哈希值
        hash_value = (
            self.h0.to_bytes(4, byteorder='big') +
            self.h1.to_bytes(4, byteorder='big') +
            self.h2.to_bytes(4, byteorder='big') +
            self.h3.to_bytes(4, byteorder='big') +
            self.h4.to_bytes(4, byteorder='big')
        )
        
        return hash_value.hex()
    
    def hash_file(self, filename):
        """
        计算文件的SHA-1哈希值
        :param filename: 文件路径
        :return: 160位哈希值（十六进制字符串）
        """
        with open(filename, 'rb') as f:
            content = f.read()
        return self.hash(content)


def test_sha1():
    """测试SHA-1算法"""
    print("=" * 60)
    print("SHA-1 哈希算法测试")
    print("=" * 60)
    
    sha1 = SHA1()
    
    # 测试用例1：空字符串
    print("\n测试1: 空字符串")
    print("-" * 60)
    message1 = ""
    hash1 = sha1.hash(message1)
    print(f"消息: (空字符串)")
    print(f"SHA-1: {hash1}")
    print(f"预期: da39a3ee5e6b4b0d3255bfef95601890afd80709")
    print(f"验证: {'✓ 通过' if hash1 == 'da39a3ee5e6b4b0d3255bfef95601890afd80709' else '✗ 失败'}")
    
    # 测试用例2：简单字符串
    print("\n测试2: 'abc'")
    print("-" * 60)
    message2 = "abc"
    hash2 = sha1.hash(message2)
    print(f"消息: {message2}")
    print(f"SHA-1: {hash2}")
    print(f"预期: a9993e364706816aba3e25717850c26c9cd0d89d")
    print(f"验证: {'✓ 通过' if hash2 == 'a9993e364706816aba3e25717850c26c9cd0d89d' else '✗ 失败'}")
    
    # 测试用例3：较长字符串
    print("\n测试3: 'Hello SHA-1 Algorithm!'")
    print("-" * 60)
    message3 = "Hello SHA-1 Algorithm!"
    hash3 = sha1.hash(message3)
    print(f"消息: {message3}")
    print(f"SHA-1: {hash3}")
    
    # 测试用例4：较长的字符串
    print("\n测试4: 较长字符串")
    print("-" * 60)
    message4 = "The quick brown fox jumps over the lazy dog"
    hash4 = sha1.hash(message4)
    print(f"消息: {message4}")
    print(f"SHA-1: {hash4}")
    print(f"预期: 2fd4e1c67a2d28fced849ee1bb76e7391b93eb12")
    print(f"验证: {'✓ 通过' if hash4 == '2fd4e1c67a2d28fced849ee1bb76e7391b93eb12' else '✗ 失败'}")
    
    # 测试用例5：数字
    print("\n测试5: 数字字符串")
    print("-" * 60)
    message5 = "123456789"
    hash5 = sha1.hash(message5)
    print(f"消息: {message5}")
    print(f"SHA-1: {hash5}")
    
    # 测试用例6：中文
    print("\n测试6: 中文字符串")
    print("-" * 60)
    message6 = "信息安全技术"
    hash6 = sha1.hash(message6)
    print(f"消息: {message6}")
    print(f"SHA-1: {hash6}")
    
    # 验证哈希的一致性
    print("\n测试7: 验证相同输入产生相同哈希")
    print("-" * 60)
    hash7a = sha1.hash("test")
    hash7b = sha1.hash("test")
    print(f"第一次哈希: {hash7a}")
    print(f"第二次哈希: {hash7b}")
    print(f"验证: {'✓ 一致' if hash7a == hash7b else '✗ 不一致'}")
    
    # 验证不同输入产生不同哈希
    print("\n测试8: 验证不同输入产生不同哈希")
    print("-" * 60)
    hash8a = sha1.hash("test")
    hash8b = sha1.hash("Test")
    print(f"'test'的哈希: {hash8a}")
    print(f"'Test'的哈希: {hash8b}")
    print(f"验证: {'✓ 不同' if hash8a != hash8b else '✗ 相同（错误）'}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_sha1()
