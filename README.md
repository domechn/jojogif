# jojogif

将视频转成gif，并添加标准结尾

## 安装

```bash
pip3 install -r requirement.txt
```

> Python3

#### 普通转换

```bash
py main.py --path video-path --begin 1 --end 2.2 --out-path ./ --size 350x600 --fps 20
```

fps 最大不会超过原视频的 fps

#### 添加标准结局

```bash
py main.py --path video-path --begin 1 --end 2.2 --out-path ./ --jojo true
```

#### 示例

![image/example.gif](./image/example.gif)

> 如果生成的gif过大，使用--size设置合理地大小
