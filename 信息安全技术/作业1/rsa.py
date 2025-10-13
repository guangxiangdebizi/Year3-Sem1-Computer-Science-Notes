"""
RSA (Rivest-Shamir-Adleman) 算法手动实现
不使用任何第三方加密库，从底层实现RSA算法
"""

import random


class RSA:
    """RSA加密算法实现类"""
    
    def __init__(self, key_size=512):
        """
        初始化RSA对象
        :param key_size: 密钥长度（位）
        """
        self.key_size = key_size
        self.public_key = None
        self.private_key = None
    
    def _is_prime(self, n, k=5):
        """
        Miller-Rabin素性检测
        :param n: 待检测的数
        :param k: 检测轮数
        :return: True表示可能是素数，False表示一定不是素数
        """
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False
        
        # 将n-1表示为2^r * d的形式
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
        
        # 进行k轮测试
        for _ in range(k):
            a = random.randrange(2, n - 1)
            x = pow(a, d, n)
            
            if x == 1 or x == n - 1:
                continue
            
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        
        return True
    
    def _generate_prime(self, bits):
        """
        生成指定位数的素数
        :param bits: 素数的位数
        :return: 素数
        """
        while True:
            # 生成随机奇数
            num = random.getrandbits(bits)
            # 确保最高位为1
            num |= (1 << (bits - 1))
            # 确保为奇数
            num |= 1
            
            if self._is_prime(num):
                return num
    
    def _gcd(self, a, b):
        """
        计算最大公约数（欧几里得算法）
        :param a: 第一个数
        :param b: 第二个数
        :return: 最大公约数
        """
        while b:
            a, b = b, a % b
        return a
    
    def _extended_gcd(self, a, b):
        """
        扩展欧几里得算法
        :param a: 第一个数
        :param b: 第二个数
        :return: (gcd, x, y) 满足 ax + by = gcd
        """
        if b == 0:
            return a, 1, 0
        else:
            gcd, x1, y1 = self._extended_gcd(b, a % b)
            x = y1
            y = x1 - (a // b) * y1
            return gcd, x, y
    
    def _mod_inverse(self, e, phi):
        """
        计算模逆元
        :param e: 数字
        :param phi: 模数
        :return: e在模phi下的逆元
        """
        gcd, x, _ = self._extended_gcd(e, phi)
        if gcd != 1:
            raise ValueError("模逆元不存在")
        return x % phi
    
    def generate_keys(self):
        """
        生成公钥和私钥
        :return: (public_key, private_key)
        """
        print(f"正在生成 {self.key_size} 位RSA密钥对...")
        
        # 生成两个大素数p和q
        print("生成素数p...")
        p = self._generate_prime(self.key_size // 2)
        
        print("生成素数q...")
        q = self._generate_prime(self.key_size // 2)
        
        # 确保p和q不相等
        while p == q:
            q = self._generate_prime(self.key_size // 2)
        
        # 计算n = p * q
        n = p * q
        
        # 计算欧拉函数φ(n) = (p-1)(q-1)
        phi = (p - 1) * (q - 1)
        
        # 选择公钥指数e (通常选择65537)
        e = 65537
        
        # 确保e和φ(n)互质
        while self._gcd(e, phi) != 1:
            e = random.randrange(3, phi, 2)
        
        # 计算私钥指数d (d是e在模φ(n)下的逆元)
        print("计算私钥...")
        d = self._mod_inverse(e, phi)
        
        # 公钥 (e, n)
        self.public_key = (e, n)
        # 私钥 (d, n)
        self.private_key = (d, n)
        
        print("密钥生成完成！")
        
        return self.public_key, self.private_key
    
    def encrypt(self, plaintext, public_key=None):
        """
        使用公钥加密
        :param plaintext: 明文字符串
        :param public_key: 公钥 (e, n)，如果为None则使用对象的公钥
        :return: 加密后的数字列表
        """
        if public_key is None:
            public_key = self.public_key
        
        if public_key is None:
            raise ValueError("请先生成密钥或提供公钥")
        
        e, n = public_key
        
        # 将字符串转换为字节，然后转换为数字
        plaintext_bytes = plaintext.encode('utf-8')
        
        # 分块加密（每块不能超过n）
        ciphertext = []
        for byte in plaintext_bytes:
            # 加密：c = m^e mod n
            encrypted = pow(byte, e, n)
            ciphertext.append(encrypted)
        
        return ciphertext
    
    def decrypt(self, ciphertext, private_key=None):
        """
        使用私钥解密
        :param ciphertext: 加密后的数字列表
        :param private_key: 私钥 (d, n)，如果为None则使用对象的私钥
        :return: 解密后的明文字符串
        """
        if private_key is None:
            private_key = self.private_key
        
        if private_key is None:
            raise ValueError("请先生成密钥或提供私钥")
        
        d, n = private_key
        
        # 解密每个数字
        plaintext_bytes = []
        for encrypted in ciphertext:
            # 解密：m = c^d mod n
            decrypted = pow(encrypted, d, n)
            plaintext_bytes.append(decrypted)
        
        # 转换回字符串
        plaintext = bytes(plaintext_bytes).decode('utf-8')
        
        return plaintext
    
    def encrypt_number(self, message, public_key=None):
        """
        加密单个数字
        :param message: 要加密的数字
        :param public_key: 公钥
        :return: 加密后的数字
        """
        if public_key is None:
            public_key = self.public_key
        
        if public_key is None:
            raise ValueError("请先生成密钥或提供公钥")
        
        e, n = public_key
        
        if message >= n:
            raise ValueError("消息太大，无法加密")
        
        return pow(message, e, n)
    
    def decrypt_number(self, ciphertext, private_key=None):
        """
        解密单个数字
        :param ciphertext: 加密后的数字
        :param private_key: 私钥
        :return: 解密后的数字
        """
        if private_key is None:
            private_key = self.private_key
        
        if private_key is None:
            raise ValueError("请先生成密钥或提供私钥")
        
        d, n = private_key
        
        return pow(ciphertext, d, n)


def test_rsa():
    """测试RSA算法"""
    print("=" * 60)
    print("RSA 加密算法测试")
    print("=" * 60)
    
    # 创建RSA对象（使用较小的密钥以加快速度）
    rsa = RSA(key_size=256)
    
    # 生成密钥对
    public_key, private_key = rsa.generate_keys()
    
    print(f"\n公钥 (e, n):")
    print(f"  e = {public_key[0]}")
    print(f"  n = {public_key[1]}")
    print(f"\n私钥 (d, n):")
    print(f"  d = {private_key[0]}")
    print(f"  n = {private_key[1]}")
    
    # 测试字符串加密
    print("\n" + "=" * 60)
    print("测试1: 字符串加密")
    print("=" * 60)
    
    plaintext = "Hello RSA!"
    print(f"\n原始明文: {plaintext}")
    
    # 加密
    print("\n正在加密...")
    ciphertext = rsa.encrypt(plaintext)
    print(f"密文(数字列表): {ciphertext}")
    
    # 解密
    print("\n正在解密...")
    decrypted = rsa.decrypt(ciphertext)
    print(f"解密后明文: {decrypted}")
    
    # 验证
    print("\n验证结果:")
    if decrypted == plaintext:
        print("✓ 加密解密成功！明文与解密结果一致")
    else:
        print("✗ 加密解密失败！")
    
    # 测试数字加密
    print("\n" + "=" * 60)
    print("测试2: 数字加密")
    print("=" * 60)
    
    message_num = 12345
    print(f"\n原始数字: {message_num}")
    
    # 加密
    print("\n正在加密...")
    encrypted_num = rsa.encrypt_number(message_num)
    print(f"加密后: {encrypted_num}")
    
    # 解密
    print("\n正在解密...")
    decrypted_num = rsa.decrypt_number(encrypted_num)
    print(f"解密后: {decrypted_num}")
    
    # 验证
    print("\n验证结果:")
    if decrypted_num == message_num:
        print("✓ 数字加密解密成功！")
    else:
        print("✗ 数字加密解密失败！")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_rsa()
