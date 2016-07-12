# Boxopus-API

你懂得，国外一家做种子离线下载的网站。不像国内某迅、某度下载学习资料会被和谐，唯一缺点就是不能够秒下。

## Requirements

* Python 2.7
* Works on Linux, Windows, Mac OSX, BSD

## Usage

### 安装依赖

```
pip install -r requirements.txt
```

### 登录的例子

```python
>>> from boxopusapi import Boxopus
>>> boxopus = Boxopus('username','password')
```

### 获取所有任务列表

```python
>>> from boxopusapi import Boxopus
>>> boxopus = Boxopus('username','password')
>>> print boxopus.getTask()
```

* 控制台输出：

```json
{
    "downloaded": [
        {
            "status": "1.49 GB (27d 6h 51m  left)",
            "link": "/torrent/75a9aeb5b81014ec5ff591df03558f97930e9c8a",
            "file_count": "3 files",
            "name": "SW-274"
        },
        {
            "status": "258.11 MB (23d 15h 15m  left)",
            "link": "/torrent/42ac383aa71516c109bdb53d49139f24102b2079",
            "file_count": "1 files",
            "name": "Bad Girls 7 - Stoya.avi"
        },
    ...
    ],
    "downloading": [
        {
            "status": "1.26 GB",
            "hash": "153b0d655ba432ef6c5494bfb566aafe33257025",
            "file_count": "1 files",
            "name": "SDDE-376R"
        },
        {
            "status": "1.72 GB",
            "hash": "94e496d2499e4db18fc78079e741869047b9e271",
            "file_count": "2 files",
            "name": "SDDE-376"
        },
    ...
    ]
}
```

### 更新下载中任务的进度

```python
>>> from boxopusapi import Boxopus
>>> boxopus = Boxopus('username','password')
>>> ret = boxopus.getTask()
>>> boxopus.updateTaskInfo(ret['downloading'])
>>> print ret
```

* 控制台输出：

```json
{
    "downloaded": [
        {
            "status": "1.49 GB (27d 6h 45m  left)",
            "link": "/torrent/75a9aeb5b81014ec5ff591df03558f97930e9c8a",
            "file_count": "3 files",
            "name": "SW-274"
        },
        {
            "status": "258.11 MB (23d 15h 9m  left)",
            "link": "/torrent/42ac383aa71516c109bdb53d49139f24102b2079",
            "file_count": "1 files",
            "name": "Bad Girls 7 - Stoya.avi"
        },
    ...
    ],
    "downloading": [
        {
            "status": "1.26 GB",
            "hash": "153b0d655ba432ef6c5494bfb566aafe33257025",
            "percentDone": 95.66,
            "file_count": "1 files",
            "name": "SDDE-376R"
        },
        {
            "status": "1.72 GB",
            "hash": "94e496d2499e4db18fc78079e741869047b9e271",
            "percentDone": 8.43,
            "file_count": "2 files",
            "name": "SDDE-376"
        },
    ...
    ]
}
```

### 创建种子任务

```python
>>> from boxopusapi import Boxopus
>>> boxopus = Boxopus('username','password')
>>> try:
>>>    path = boxopus.uploadTorrent('SDDE-376R.torrent')
>>>    boxopus.createTask(path)
>>>    print('已创建种子任务')
>>> except Exception, e:
>>>    print('种子解析失败')
```

## TODOS

* [ ] 创建磁力链接任务
* [ ] 完善cookie失效重登机制
* [ ] 打包上传到PyPI
* [ ] 集成到Alfred
