@echo off
chcp 65001
echo ========================================
echo 信息安全技术实验 - 经典密码算法测试
echo ========================================
echo.
echo 开始运行测试程序...
echo.

echo [1/4] 运行 DES 算法测试...
python des.py
echo.

echo [2/4] 运行 RSA 算法测试...
python rsa.py
echo.

echo [3/4] 运行 SHA-1 算法测试...
python sha1.py
echo.

echo [4/4] 运行综合测试...
python main.py
echo.

echo 所有测试完成！
pause
