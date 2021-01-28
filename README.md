# infoscaner

## 环境配置

infoscaner是基于python3版本实现的，运行之前首先安装python库

如果同时存在python2和python3,请输入以下命令

```powershell
pip3 install -r requirements.txt
```

如果仅有python3且未重命名exe文件，可以使用

```powershell
pip install -r requirements.txt
```

infoscaner在主机扫描时调用了Nmap，请安装Nmap

## 使用方法

### 获取帮助信息

```powershell
python3 infoscaner.py -h
```

![image-20201006103648177](C:\Users\19711\AppData\Roaming\Typora\typora-user-images\image-20201006103648177.png)

### 默认扫描目标信息(WHOIS扫描)

```powershell
python3 infoscaner.py -u vulnweb.com
```

![image-20201006103813786](C:\Users\19711\AppData\Roaming\Typora\typora-user-images\image-20201006103813786.png)

### 获取旁站或C站信息

```powershell
python3 infoscaner.py -u vulnweb.com -N
```

![image-20201006103944217](C:\Users\19711\AppData\Roaming\Typora\typora-user-images\image-20201006103944217.png)

### 获取CMS指纹信息

```powershell
python3 infoscaner.py -u vulnweb.com -C
```

![image-20201006104108785](C:\Users\19711\AppData\Roaming\Typora\typora-user-images\image-20201006104108785.png)

### 获取ICP备案号

```powershell
python3 infoscaner.py -u baidu.com -i
```

![image-20201006104610470](C:\Users\19711\AppData\Roaming\Typora\typora-user-images\image-20201006104610470.png)

### 获取nslookup信息

```powershell
python3 infoscaner.py -u testphp.vulnweb.com -n
```

![image-20201006104748962](C:\Users\19711\AppData\Roaming\Typora\typora-user-images\image-20201006104748962.png)

### 获取全部信息

```
python3 infoscaner.py -u testphp.vulnweb.com -A
```

![image-20201006104842301](C:\Users\19711\AppData\Roaming\Typora\typora-user-images\image-20201006104842301.png)

### 默认目录扫描

```
python3 infoscaner.py -u 192.168.2.128 -d all
```

![image-20201006105425336](C:\Users\19711\AppData\Roaming\Typora\typora-user-images\image-20201006105425336.png)

### 目录扫描设置线程

```powershell
python3 infoscaner.py -u 192.168.2.128 -d all -t 15
```

![image-20201006105541416](C:\Users\19711\AppData\Roaming\Typora\typora-user-images\image-20201006105541416.png)

### FTP和SSH弱口令扫描

```powershell
python3 infoscaner.py -u 192.168.2.207 -W
```

![image-20201006110213244](C:\Users\19711\AppData\Roaming\Typora\typora-user-images\image-20201006110213244.png)

### 简单whois输出

```powershell
python3 infoscaner.py -u www.baidu.com -w -o
```

![image-20201006110320399](C:\Users\19711\AppData\Roaming\Typora\typora-user-images\image-20201006110320399.png)

其他输出同理

### 全面扫描

```
python3 infoscaner.py -u 192.168.2.1 -a
```

![image-20201006111530697](C:\Users\19711\AppData\Roaming\Typora\typora-user-images\image-20201006111530697.png)

### 指定端口扫描

```
python3 infoscaner.py -u 192.168.2.1 -p 80,445
```

![image-20201006111608215](C:\Users\19711\AppData\Roaming\Typora\typora-user-images\image-20201006111608215.png)

## 获取子域名

```
 python3 infoscaner.py -u ./scan_file/target.txt -s
```

![image-20201109142714634](C:\Users\19711\AppData\Roaming\Typora\typora-user-images\image-20201109142714634.png)

## 获取子域名并输出

```
 python3 infoscaner.py -u ./scan_file/target.txt -s -o
```

![image-20201109144830475](C:\Users\19711\AppData\Roaming\Typora\typora-user-images\image-20201109144830475.png)

