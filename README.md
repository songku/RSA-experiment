# RSA-experiment
拖拖拉拉，copy代码，凑成的实验结果

# 需要注意
str通过encode()函数，再通过bytes2int得到的数字应该小于公钥的n，不然会失真。
有几个对长字符加密的初步想法，bytes分片处理，每个的加密结果保存在数组里面。解密对数组中每个元素，进行分别解密，得到的byetes拼凑在一起，再decode。

# 加密逻辑
用户输入str类型字符串，通过encode，编码为字节，调用bytes2int转为int,根据公钥(n,e)加密得到数字。

# 解密逻辑
根据用户输入的数字，使用私钥(n,d)，得到解密后的int，调用int2bytes转为字节，再通过decode转为str类型的原明文字符串。

＃ prime.py
给出的欧几里得算法和扩展欧几里得算法给出了生成素数和求模反元素的方法

#str2long.py
copy了官方代码的对bytes2int和int2bytes的实现

# RSA_CANKAO.py
给出了基本代码

# RSA_keylength_changed.py
改变了密钥长度，生成的n的长度修改为了rand.randint(keylength//2,keylength)。而keylength设定为了2**20。

# RSA_outcome.py
给出了几个测试样例

# RSA算法实验笔记.md
给出了一些博客给自己的启发，以及一些算法实现的理解方法，较通俗易懂，帮助很大
