import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

from des import DES
from rsa import RSA
from sha1 import SHA1


class CryptoGUI:
    """经典密码算法图形化演示工具"""

    def __init__(self, master):
        self.master = master
        master.title("信息安全技术实验 - 经典密码算法演示")
        master.geometry("900x700")

        self.rsa_instance = None

        notebook = ttk.Notebook(master)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # DES 标签页
        self.des_frame = ttk.Frame(notebook)
        notebook.add(self.des_frame, text="DES 加密/解密")
        self._build_des_tab()

        # RSA 标签页
        self.rsa_frame = ttk.Frame(notebook)
        notebook.add(self.rsa_frame, text="RSA 加密/解密")
        self._build_rsa_tab()

        # SHA-1 标签页
        self.sha_frame = ttk.Frame(notebook)
        notebook.add(self.sha_frame, text="SHA-1 摘要")
        self._build_sha_tab()

        # 综合演示
        self.demo_frame = ttk.Frame(notebook)
        notebook.add(self.demo_frame, text="综合安全通信演示")
        self._build_demo_tab()

    # ----------------------- DES -----------------------
    def _build_des_tab(self):
        ttk.Label(self.des_frame, text="DES 密钥 (8 字节):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.des_key_entry = ttk.Entry(self.des_frame, width=30)
        self.des_key_entry.insert(0, "SECRET01")
        self.des_key_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(self.des_frame, text="明文:").grid(row=1, column=0, sticky=tk.NW, padx=5, pady=5)
        self.des_plaintext_text = scrolledtext.ScrolledText(self.des_frame, width=60, height=6)
        self.des_plaintext_text.insert(tk.END, "信息安全技术 DES 测试")
        self.des_plaintext_text.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

        encrypt_button = ttk.Button(self.des_frame, text="执行加密", command=self.des_encrypt)
        encrypt_button.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(self.des_frame, text="密文(十六进制):").grid(row=3, column=0, sticky=tk.NW, padx=5, pady=5)
        self.des_cipher_text = scrolledtext.ScrolledText(self.des_frame, width=60, height=6)
        self.des_cipher_text.grid(row=3, column=1, columnspan=3, padx=5, pady=5)

        decrypt_button = ttk.Button(self.des_frame, text="执行解密", command=self.des_decrypt)
        decrypt_button.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(self.des_frame, text="解密结果:").grid(row=5, column=0, sticky=tk.NW, padx=5, pady=5)
        self.des_decrypted_text = scrolledtext.ScrolledText(self.des_frame, width=60, height=6)
        self.des_decrypted_text.grid(row=5, column=1, columnspan=3, padx=5, pady=5)

    def des_encrypt(self):
        key = self.des_key_entry.get()
        plaintext = self.des_plaintext_text.get("1.0", tk.END).strip()
        try:
            des = DES(key)
            ciphertext_hex = des.encrypt(plaintext)
            self.des_cipher_text.delete("1.0", tk.END)
            self.des_cipher_text.insert(tk.END, ciphertext_hex)
            messagebox.showinfo("DES 加密", "加密成功！")
        except Exception as exc:
            messagebox.showerror("DES 错误", f"加密失败: {exc}")

    def des_decrypt(self):
        key = self.des_key_entry.get()
        ciphertext_hex = self.des_cipher_text.get("1.0", tk.END).strip()
        try:
            des = DES(key)
            plaintext = des.decrypt(ciphertext_hex)
            self.des_decrypted_text.delete("1.0", tk.END)
            self.des_decrypted_text.insert(tk.END, plaintext)
            messagebox.showinfo("DES 解密", "解密成功！")
        except Exception as exc:
            messagebox.showerror("DES 错误", f"解密失败: {exc}")

    # ----------------------- RSA -----------------------
    def _build_rsa_tab(self):
        ttk.Label(self.rsa_frame, text="密钥长度 (位):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.rsa_keysize_entry = ttk.Entry(self.rsa_frame, width=10)
        self.rsa_keysize_entry.insert(0, "256")
        self.rsa_keysize_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        generate_button = ttk.Button(self.rsa_frame, text="生成RSA密钥对", command=self.rsa_generate_keys)
        generate_button.grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)

        ttk.Label(self.rsa_frame, text="公钥/私钥信息:").grid(row=1, column=0, sticky=tk.NW, padx=5, pady=5)
        self.rsa_keys_text = scrolledtext.ScrolledText(self.rsa_frame, width=70, height=10)
        self.rsa_keys_text.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

        ttk.Label(self.rsa_frame, text="明文 (字符串):").grid(row=2, column=0, sticky=tk.NW, padx=5, pady=5)
        self.rsa_plain_entry = scrolledtext.ScrolledText(self.rsa_frame, width=60, height=4)
        self.rsa_plain_entry.insert(tk.END, "Hello RSA!")
        self.rsa_plain_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5)

        encrypt_button = ttk.Button(self.rsa_frame, text="加密字符串", command=self.rsa_encrypt)
        encrypt_button.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(self.rsa_frame, text="密文 (数字列表，逗号分隔):").grid(row=4, column=0, sticky=tk.NW, padx=5, pady=5)
        self.rsa_cipher_entry = scrolledtext.ScrolledText(self.rsa_frame, width=60, height=4)
        self.rsa_cipher_entry.grid(row=4, column=1, columnspan=3, padx=5, pady=5)

        decrypt_button = ttk.Button(self.rsa_frame, text="解密字符串", command=self.rsa_decrypt)
        decrypt_button.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(self.rsa_frame, text="解密结果:").grid(row=6, column=0, sticky=tk.NW, padx=5, pady=5)
        self.rsa_decrypted_entry = scrolledtext.ScrolledText(self.rsa_frame, width=60, height=4)
        self.rsa_decrypted_entry.grid(row=6, column=1, columnspan=3, padx=5, pady=5)

    def rsa_generate_keys(self):
        try:
            key_size = int(self.rsa_keysize_entry.get())
            if key_size < 128:
                raise ValueError("密钥长度应不小于128位")
            self.rsa_instance = RSA(key_size=key_size)
            public_key, private_key = self.rsa_instance.generate_keys()
            self.rsa_keys_text.delete("1.0", tk.END)
            self.rsa_keys_text.insert(
                tk.END,
                f"公钥 (e, n):\n  e = {public_key[0]}\n  n = {public_key[1]}\n\n"
                f"私钥 (d, n):\n  d = {private_key[0]}\n  n = {private_key[1]}"
            )
            messagebox.showinfo("RSA 密钥", "密钥对生成成功！")
        except Exception as exc:
            messagebox.showerror("RSA 错误", f"生成密钥失败: {exc}")

    def rsa_encrypt(self):
        if self.rsa_instance is None or self.rsa_instance.public_key is None:
            messagebox.showwarning("RSA 提示", "请先生成RSA密钥对")
            return
        plaintext = self.rsa_plain_entry.get("1.0", tk.END).strip()
        if not plaintext:
            messagebox.showwarning("RSA 提示", "请输入待加密的明文")
            return
        try:
            ciphertext = self.rsa_instance.encrypt(plaintext)
            cipher_str = ",".join(str(num) for num in ciphertext)
            self.rsa_cipher_entry.delete("1.0", tk.END)
            self.rsa_cipher_entry.insert(tk.END, cipher_str)
            messagebox.showinfo("RSA 加密", "加密成功！")
        except Exception as exc:
            messagebox.showerror("RSA 错误", f"加密失败: {exc}")

    def rsa_decrypt(self):
        if self.rsa_instance is None or self.rsa_instance.private_key is None:
            messagebox.showwarning("RSA 提示", "请先生成RSA密钥对")
            return
        cipher_text = self.rsa_cipher_entry.get("1.0", tk.END).strip()
        if not cipher_text:
            messagebox.showwarning("RSA 提示", "请输入密文数字列表")
            return
        try:
            cipher_nums = [int(num.strip()) for num in cipher_text.split(',') if num.strip()]
            plaintext = self.rsa_instance.decrypt(cipher_nums)
            self.rsa_decrypted_entry.delete("1.0", tk.END)
            self.rsa_decrypted_entry.insert(tk.END, plaintext)
            messagebox.showinfo("RSA 解密", "解密成功！")
        except Exception as exc:
            messagebox.showerror("RSA 错误", f"解密失败: {exc}")

    # ----------------------- SHA-1 -----------------------
    def _build_sha_tab(self):
        ttk.Label(self.sha_frame, text="输入消息:").grid(row=0, column=0, sticky=tk.NW, padx=5, pady=5)
        self.sha_input_text = scrolledtext.ScrolledText(self.sha_frame, width=70, height=6)
        self.sha_input_text.insert(tk.END, "The quick brown fox jumps over the lazy dog")
        self.sha_input_text.grid(row=0, column=1, columnspan=3, padx=5, pady=5)

        hash_button = ttk.Button(self.sha_frame, text="计算SHA-1摘要", command=self.sha_compute)
        hash_button.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(self.sha_frame, text="SHA-1 摘要结果:").grid(row=2, column=0, sticky=tk.NW, padx=5, pady=5)
        self.sha_output_text = scrolledtext.ScrolledText(self.sha_frame, width=70, height=4)
        self.sha_output_text.grid(row=2, column=1, columnspan=3, padx=5, pady=5)

    def sha_compute(self):
        message = self.sha_input_text.get("1.0", tk.END).strip()
        if not message:
            messagebox.showwarning("SHA-1 提示", "请输入消息")
            return
        sha = SHA1()
        digest = sha.hash(message)
        self.sha_output_text.delete("1.0", tk.END)
        self.sha_output_text.insert(tk.END, digest)

    # ----------------------- 综合演示 -----------------------
    def _build_demo_tab(self):
        ttk.Label(self.demo_frame, text="原始消息:").grid(row=0, column=0, sticky=tk.NW, padx=5, pady=5)
        self.demo_message_text = scrolledtext.ScrolledText(self.demo_frame, width=70, height=4)
        self.demo_message_text.insert(tk.END, "这是一条重要的机密信息！")
        self.demo_message_text.grid(row=0, column=1, columnspan=4, padx=5, pady=5)

        ttk.Label(self.demo_frame, text="DES 密钥:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.demo_des_key_entry = ttk.Entry(self.demo_frame, width=20)
        self.demo_des_key_entry.insert(0, "SECRET01")
        self.demo_des_key_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(self.demo_frame, text="RSA 密钥长度:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.demo_rsa_keysize_entry = ttk.Entry(self.demo_frame, width=10)
        self.demo_rsa_keysize_entry.insert(0, "256")
        self.demo_rsa_keysize_entry.grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)

        demo_button = ttk.Button(self.demo_frame, text="执行综合演示", command=self.run_demo)
        demo_button.grid(row=1, column=4, sticky=tk.W, padx=5, pady=5)

        ttk.Label(self.demo_frame, text="演示日志:").grid(row=2, column=0, sticky=tk.NW, padx=5, pady=5)
        self.demo_log_text = scrolledtext.ScrolledText(self.demo_frame, width=100, height=22)
        self.demo_log_text.grid(row=2, column=1, columnspan=4, padx=5, pady=5)

    def run_demo(self):
        message = self.demo_message_text.get("1.0", tk.END).strip()
        des_key = self.demo_des_key_entry.get()
        try:
            rsa_bits = int(self.demo_rsa_keysize_entry.get())
        except ValueError:
            messagebox.showerror("综合演示", "RSA 密钥长度必须为整数")
            return

        if not message:
            messagebox.showwarning("综合演示", "请输入原始消息")
            return

        log_lines = []
        try:
            log_lines.append("[1] 原始消息: " + message)

            # SHA-1 摘要
            sha = SHA1()
            digest = sha.hash(message)
            log_lines.append("[2] 消息摘要 (SHA-1): " + digest)

            # DES 加密
            des = DES(des_key)
            ciphertext = des.encrypt(message)
            log_lines.append("[3] DES 加密结果 (十六进制): " + ciphertext)

            # RSA 加密 DES 密钥
            rsa = RSA(key_size=rsa_bits)
            rsa.generate_keys()
            encrypted_key = rsa.encrypt(des_key)
            log_lines.append("[4] RSA 加密的 DES 密钥: " + ",".join(str(x) for x in encrypted_key))

            # 解密流程
            decrypted_key = rsa.decrypt(encrypted_key)
            log_lines.append("[5] RSA 解密得到的 DES 密钥: " + decrypted_key)

            des_for_decrypt = DES(decrypted_key)
            decrypted_message = des_for_decrypt.decrypt(ciphertext)
            log_lines.append("[6] DES 解密得到的原始消息: " + decrypted_message)

            verify_digest = sha.hash(decrypted_message)
            log_lines.append("[7] 解密消息摘要 (SHA-1): " + verify_digest)

            if decrypted_message == message and verify_digest == digest:
                log_lines.append("[8] 验证结果: ✔ 消息一致，摘要一致，传输安全可靠")
            else:
                log_lines.append("[8] 验证结果: ✘ 验证失败，请检查实现")

            messagebox.showinfo("综合演示", "综合演示完成！详情见日志。")
        except Exception as exc:
            log_lines.append(f"[!] 演示过程中发生错误: {exc}")
            messagebox.showerror("综合演示", f"执行失败: {exc}")

        self.demo_log_text.delete("1.0", tk.END)
        self.demo_log_text.insert(tk.END, "\n".join(log_lines))


def main():
    root = tk.Tk()
    CryptoGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
