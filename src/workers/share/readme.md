## 预警模块说明

### server类
- 位置：
server.py
- 作用：
mq的消费者，无限循环监听队列消息，并且将消息传递给handler类处理
- 抽象：
提供run方法启动服务
- 主要类：
SyncAlertServer、AsyncAlertServer
***
### handler类
- 位置：
handler.py
- 作用：
从server类获取消息，封装之后传给过滤器，过滤后传递给所有观察者（viewer类）
- 抽象：
提供do_handle方法处理消息，动态添加移除观察者，动态添加移除过滤器
- 主要类：
AlertMessageHandler
***
### filter类
- 位置：
filter.py
- 作用：
过滤消息
- 抽象：
提供filter方法，返回True表明无需过滤，返回False表明需要过滤
- 主要类：
AlertFilter, DistinctFilter
***
### viewer类
- 位置：
viewer.py
- 作用：
消息观察者，根据消息执行相应的动作
- 抽象：
提供update方法,接收消息并且执行相应动作
- 主要类：
MysqlViewer、QueueViewer、ShortMessageViewer、WechatViewer
### message类
- 位置：
viewer.py
- 作用：
封装消息，提供统一的对象给消息观察者(viewer)以及过滤器(filter)使用
- 抽象：
__init__方法接收原始消息并进行相应的处理
- 主要类：
Message
