"""
信息安全技术实验 - 经典密码算法实现
包含DES、RSA、SHA-1三种算法的完整实现和测试
"""

from des import DES, test_des
from rsa import RSA, test_rsa
from sha1 import SHA1, test_sha1


def print_header(title):
    """打印标题"""
    print("\n" + "=" * 80)
    print(title.center(80))
    print("=" * 80 + "\n")


def main():
    """主函数：运行所有测试"""
    print_header("信息安全技术实验 - 经典密码算法实现")
    print("实验内容：")
    print("  1. DES (Data Encryption Standard) 加密算法")
    print("  2. RSA (Rivest-Shamir-Adleman) 加密算法")
    print("  3. SHA-1 (Secure Hash Algorithm 1) 哈希算法")
    print("\n说明：所有算法均为手动实现，未使用第三方加密库\n")
    
    input("按Enter键开始测试DES算法...")
    
    # 测试1：DES算法
    print_header("实验一：DES加密算法")
    test_des()
    
    input("\n按Enter键开始测试RSA算法...")
    
    # 测试2：RSA算法
    print_header("实验二：RSA加密算法")
    test_rsa()
    
    input("\n按Enter键开始测试SHA-1算法...")
    
    # 测试3：SHA-1算法
    print_header("实验三：SHA-1哈希算法")
    test_sha1()
    
    # 综合测试
    input("\n按Enter键开始综合测试...")
    print_header("综合应用测试")
    
    print("场景：使用三种算法进行安全通信")
    print("-" * 80)
    
    # 1. 创建原始消息
    original_message = "这是一条重要的机密信息！"
    print(f"\n1. 原始消息: {original_message}")
    
    # 2. 使用SHA-1计算消息摘要
    print("\n2. 使用SHA-1计算消息摘要...")
    sha1 = SHA1()
    message_digest = sha1.hash(original_message)
    print(f"   消息摘要: {message_digest}")
    
    # 3. 使用DES加密消息
    print("\n3. 使用DES加密消息...")
    des_key = "SECRET01"
    des = DES(des_key)
    encrypted_message = des.encrypt(original_message)
    print(f"   DES密钥: {des_key}")
    print(f"   加密结果: {encrypted_message[:80]}...")
    
    # 4. 使用RSA加密DES密钥
    print("\n4. 使用RSA加密DES密钥...")
    rsa = RSA(key_size=256)
    rsa.generate_keys()
    encrypted_key = rsa.encrypt(des_key)
    print(f"   加密的密钥: {encrypted_key}")
    
    # 5. 解密过程
    print("\n5. 解密过程...")
    print("   5.1 使用RSA私钥解密DES密钥...")
    decrypted_key = rsa.decrypt(encrypted_key)
    print(f"       解密的密钥: {decrypted_key}")
    
    print("   5.2 使用DES密钥解密消息...")
    des2 = DES(decrypted_key)
    decrypted_message = des2.decrypt(encrypted_message)
    print(f"       解密的消息: {decrypted_message}")
    
    print("   5.3 验证消息完整性（计算摘要）...")
    decrypted_digest = sha1.hash(decrypted_message)
    print(f"       解密消息摘要: {decrypted_digest}")
    
    # 6. 验证
    print("\n6. 验证结果:")
    print(f"   原始消息 == 解密消息: {'✓ 是' if original_message == decrypted_message else '✗ 否'}")
    print(f"   原始摘要 == 解密摘要: {'✓ 是' if message_digest == decrypted_digest else '✗ 否'}")
    
    if original_message == decrypted_message and message_digest == decrypted_digest:
        print("\n   ✓ 综合测试通过！消息传输安全且完整！")
    else:
        print("\n   ✗ 综合测试失败！")
    
    print("\n" + "=" * 80)
    print("实验完成！".center(80))
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
