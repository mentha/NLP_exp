# NLP

本项目为BIT NLP作业

## 项目介绍

本项目主要完成分词和词性标注功能

 * 分词通过n元语法模型实现

 * 词性标注通过HMM模型实现
 
## 代码组织

 * cut.py为分词模块
 
 * mark.py为词性标注模块
 
 * tool.py使用上述两个模块对字符串进行分词并判断词性
 
 * 其他源文件用来产生词典
 
 * *.json.xz 为压缩后的词典

## 使用方法

```
>>> from NLP import Scissor
>>> s = Scissor(json.loads(lzma.open('NLP/wf.json.xz').read().decode('UTF-8')), json.loads(lzma.open('NLP/iw.json.xz').read().decode('UTF-8')))
>>> s.Cut('自然语言处理是人工智能和语言学领域的分支学科。')
['自然', '语言', '处理', '是', '人工', '智能', '和', '语言', '学', '领域', '的', '分支', '学科', '。']
```

```
>>> from NLP import Mark
>>> m = Mark(json.loads(lzma.open('pos.json.xz').read().decode('utf-8')), json.loads(lzma.open('bposf.json.xz').read().decode('utf-8')), json.loads(lzma.open('iposf.json.xz').read().decode('utf-8')))
>>> m.Sentemark(['自然', '语言', '通常', '是', '指', '一种', '自然', '地', '随', '文化', '演化', '的', '语言', '。'])
['n', 'n', 'd', 'vshi', 'v', 'mq', 'n', 'ude2', 'p', 'n', 'vn', 'ude1', 'n', 'w']
```
