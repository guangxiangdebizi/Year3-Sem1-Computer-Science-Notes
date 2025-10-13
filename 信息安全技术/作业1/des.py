"""
DES (Data Encryption Standard) 算法手动实现
不使用任何第三方加密库，从底层实现DES算法
"""


class DES:
    """DES加密算法实现类"""
    
    # 初始置换表 (Initial Permutation)
    IP = [
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7
    ]
    
    # 逆初始置换表 (Final Permutation)
    FP = [
        40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25
    ]
    
    # 扩展置换表 (Expansion)
    E = [
        32, 1, 2, 3, 4, 5,
        4, 5, 6, 7, 8, 9,
        8, 9, 10, 11, 12, 13,
        12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32, 1
    ]
    
    # P置换表
    P = [
        16, 7, 20, 21, 29, 12, 28, 17,
        1, 15, 23, 26, 5, 18, 31, 10,
        2, 8, 24, 14, 32, 27, 3, 9,
        19, 13, 30, 6, 22, 11, 4, 25
    ]
    
    # S盒
    S_BOX = [
        # S1
        [
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
        ],
        # S2
        [
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
        ],
        # S3
        [
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
        ],
        # S4
        [
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
        ],
        # S5
        [
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
        ],
        # S6
        [
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
        ],
        # S7
        [
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
        ],
        # S8
        [
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
        ]
    ]
    
    # 密钥置换选择1 (PC-1)
    PC1 = [
        57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4
    ]
    
    # 密钥置换选择2 (PC-2)
    PC2 = [
        14, 17, 11, 24, 1, 5,
        3, 28, 15, 6, 21, 10,
        23, 19, 12, 4, 26, 8,
        16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 46, 54,
        29, 36, 45, 50, 38, 32,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32
    ]
    
    # 每轮密钥循环左移的位数
    SHIFT = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
    
    def __init__(self, key):
        """
        初始化DES对象
        :param key: 8字节密钥
        """
        if isinstance(key, str):
            key_bytes = key.encode('utf-8')
        else:
            key_bytes = bytes(key)
        if len(key_bytes) != 8:
            raise ValueError("DES密钥必须为8字节")
        self.key = key_bytes
        self.sub_keys = self._generate_sub_keys()
    
    def _bytes_to_bits(self, data):
        """将字节序列转换为比特列表"""
        bits = []
        for byte in data:
            for i in range(7, -1, -1):
                bits.append((byte >> i) & 1)
        return bits
    
    def _bits_to_bytes(self, bits):
        """将比特列表转换为字节序列"""
        result = bytearray()
        for i in range(0, len(bits), 8):
            byte = 0
            for j in range(8):
                if i + j < len(bits):
                    byte = (byte << 1) | bits[i + j]
            result.append(byte)
        return bytes(result)
    
    def _permute(self, block, table):
        """根据置换表进行置换"""
        return [block[i - 1] for i in table]
    
    def _xor(self, bits1, bits2):
        """异或操作"""
        return [b1 ^ b2 for b1, b2 in zip(bits1, bits2)]
    
    def _left_shift(self, bits, n):
        """循环左移"""
        return bits[n:] + bits[:n]
    
    def _generate_sub_keys(self):
        """生成16个子密钥"""
        # 将密钥转换为比特
        key_bits = self._bytes_to_bits(self.key)
        
        # PC-1置换
        key_bits = self._permute(key_bits, self.PC1)
        
        # 分为左右两部分
        C = key_bits[:28]
        D = key_bits[28:]
        
        sub_keys = []
        for i in range(16):
            # 循环左移
            C = self._left_shift(C, self.SHIFT[i])
            D = self._left_shift(D, self.SHIFT[i])
            
            # PC-2置换
            sub_key = self._permute(C + D, self.PC2)
            sub_keys.append(sub_key)
        
        return sub_keys
    
    def _f_function(self, right, sub_key):
        """F函数"""
        # E扩展
        expanded = self._permute(right, self.E)
        
        # 与子密钥异或
        xored = self._xor(expanded, sub_key)
        
        # S盒替换
        output = []
        for i in range(8):
            # 6位一组
            block = xored[i * 6:(i + 1) * 6]
            
            # 计算行和列
            row = (block[0] << 1) | block[5]
            col = (block[1] << 3) | (block[2] << 2) | (block[3] << 1) | block[4]
            
            # S盒查找
            val = self.S_BOX[i][row][col]
            
            # 转换为4位
            for j in range(3, -1, -1):
                output.append((val >> j) & 1)
        
        # P置换
        return self._permute(output, self.P)
    
    def _process_block(self, block, sub_keys):
        """处理一个64位数据块"""
        # 初始置换
        block = self._permute(block, self.IP)
        
        # 分为左右两部分
        left = block[:32]
        right = block[32:]
        
        # 16轮迭代
        for i in range(16):
            temp = right[:]
            right = self._xor(left, self._f_function(right, sub_keys[i]))
            left = temp
        
        # 交换左右
        combined = right + left
        
        # 逆初始置换
        return self._permute(combined, self.FP)
    
    def encrypt(self, plaintext):
        """
        加密明文
        :param plaintext: 明文（字符串或字节串）
        :return: 加密后的十六进制字符串
        """
        if isinstance(plaintext, str):
            plaintext_bytes = plaintext.encode('utf-8')
        else:
            plaintext_bytes = bytes(plaintext)
        
        # PKCS#7填充
        pad_len = 8 - (len(plaintext_bytes) % 8)
        if pad_len == 0:
            pad_len = 8
        plaintext_bytes += bytes([pad_len] * pad_len)
        
        ciphertext_bits = []
        
        # 分块加密
        for i in range(0, len(plaintext_bytes), 8):
            block = plaintext_bytes[i:i + 8]
            block_bits = self._bytes_to_bits(block)
            encrypted_block = self._process_block(block_bits, self.sub_keys)
            ciphertext_bits.extend(encrypted_block)
        
        # 转换为十六进制
        hex_str = ''
        for i in range(0, len(ciphertext_bits), 4):
            val = 0
            for j in range(4):
                if i + j < len(ciphertext_bits):
                    val = (val << 1) | ciphertext_bits[i + j]
            hex_str += format(val, 'X')
        
        return hex_str
    
    def decrypt(self, ciphertext_hex):
        """
        解密密文
        :param ciphertext_hex: 十六进制密文字符串
        :return: 解密后的明文字符串
        """
        # 将十六进制转换为比特
        ciphertext_bits = []
        for hex_char in ciphertext_hex:
            val = int(hex_char, 16)
            for i in range(3, -1, -1):
                ciphertext_bits.append((val >> i) & 1)
        
        plaintext_bytes = bytearray()
        
        # 使用逆序的子密钥进行解密
        reversed_keys = self.sub_keys[::-1]
        
        # 分块解密
        for i in range(0, len(ciphertext_bits), 64):
            block = ciphertext_bits[i:i + 64]
            if len(block) == 64:
                decrypted_block_bits = self._process_block(block, reversed_keys)
                plaintext_bytes.extend(self._bits_to_bytes(decrypted_block_bits))
        
        if not plaintext_bytes:
            return ''
        
        # 移除PKCS#7填充
        pad_len = plaintext_bytes[-1]
        if pad_len < 1 or pad_len > 8:
            raise ValueError("解密填充无效")
        if plaintext_bytes[-pad_len:] != bytes([pad_len] * pad_len):
            raise ValueError("解密填充校验失败")
        plaintext_bytes = plaintext_bytes[:-pad_len]
        
        return plaintext_bytes.decode('utf-8')


def test_des():
    """测试DES算法"""
    print("=" * 60)
    print("DES 加密算法测试")
    print("=" * 60)
    
    # 测试用例
    key = "DESKEY12"  # 8字节密钥
    plaintext = "Hello DES Algorithm!"
    
    print(f"\n原始密钥: {key}")
    print(f"原始明文: {plaintext}")
    print(f"明文长度: {len(plaintext)} 字节")
    
    # 创建DES对象
    des = DES(key)
    
    # 加密
    print("\n正在加密...")
    ciphertext = des.encrypt(plaintext)
    print(f"密文(十六进制): {ciphertext}")
    
    # 解密
    print("\n正在解密...")
    decrypted = des.decrypt(ciphertext)
    print(f"解密后明文: {decrypted}")
    
    # 验证
    print("\n验证结果:")
    if decrypted == plaintext:
        print("✓ 加密解密成功！明文与解密结果一致")
    else:
        print("✗ 加密解密失败！")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_des()
