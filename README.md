# NLP

本项目为BIT NLP作业

本项目使用的语料库为人民日报2014

## 项目介绍

本项目主要完成分词和词性标注功能

 * 分词通过n元语法模型实现

 * 词性标注通过HMM模型实现
 
## 代码组织

 * cut.py为分词模块
 
 * mark.py为词性标注模块
 
 * tool.py使用上述两个模块对字符串进行分词并判断词性
 
 * dictgen中的源文件用来产生词典
 
 * *.json.xz 为压缩后的词典

## 使用方法

```
>>> from NLP import Scissor
>>> s = Scissor(json.loads(lzma.open('NLP/wf.json.xz').read().decode('UTF-8')), json.loads(lzma.open('NLP/iw.json.xz').read().decode('UTF-8')))
>>> s.Cut('自然语言通常是指一种自然地随文化演化的语言。')
['自然', '语言', '通常', '是', '指', '一种', '自然', '地', '随', '文化', '演化', '的', '语言', '。']
```

```
>>> from NLP import Mark
>>> m = Mark(json.loads(lzma.open('NLP/pos.json.xz').read().decode('utf-8')), json.loads(lzma.open('NLP/bposf.json.xz').read().decode('utf-8')), json.loads(lzma.open('NLP/iposf.json.xz').read().decode('utf-8')))
>>> m.Sentemark(['自然', '语言', '通常', '是', '指', '一种', '自然', '地', '随', '文化', '演化', '的', '语言', '。'])
['n', 'n', 'd', 'vshi', 'v', 'mq', 'n', 'ude2', 'p', 'n', 'vn', 'ude1', 'n', 'w']
```

```
>>> from NLP import tool
>>> t = tool.Tool()
>>> t.Cut_mark('自然语言通常是指一种自然地随文化演化的语言。')
['自然/n', '语言/n', '通常/d', '是/vshi', '指/v', '一种/mq', '自然/n', '地/ude2', '随/p', '文化/n', '演化/vn', '的/ude1', '语言/n', '。/w']
```
