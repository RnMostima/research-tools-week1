# research-tools-week1

git与GitHub上传管理练习

网页端修改readme并进行查看

## 词频统计程序

`code/word_freq.py` 可以统计英文文本中单词出现的次数，忽略大小写和标点，并支持带撇号或连字符的单词。

统计指定文件并显示前 10 个高频词：

```powershell
python .\code\word_freq.py .\text.txt --top 10
```

从标准输入读取文本：

```powershell
Get-Content .\text.txt | python .\code\word_freq.py -
```

显示全部单词：

```powershell
python .\code\word_freq.py .\text.txt --all
```