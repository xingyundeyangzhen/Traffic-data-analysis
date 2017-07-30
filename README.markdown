# Traffic data analysis and Visualization

## 1. 介绍
这是一个用Flask实现简单粗糙的后端，用D3.js和Bootstrap实现前端的交通大数据显示系统。测试的数据源为csv格式，包含104万条交通数据。后端实现的功能包括用户的登陆和注册，以及数据显示范围的筛选。前端实现的功能是对交通数据的各种图表显示，其中包括交通流量图、平行坐标图、散点图以及原始数据表格的展示。数据文件的下载地址是[这里](http://pan.baidu.com/s/1kUJJl7h)

## 2. 实现
后端基于flask框架实现，实现了简单的用户注册和登陆功能。实现了响应前端提交的请求并且根据请求的参数返回用于数据筛选的json格式的参数。

+ 登陆和注册功能的实现如下：
```
@app.route('/register', methods=['post', 'get'])
@app.route('/login', methods=['post', 'get'])
def handle_login():
    username = request.form.get('username', None)
    pswd = request.form.get('password', None)
    if request.form.get('register-submit', None) and username and pswd:
        email = request.form.get('email', None)
        if request.form.get('confirm-password') == pswd:
            u = user(username, pswd, email)
            db.session.add(u)
            db.session.commit()
        return redirect(url_for('login'))
    elif request.form.get('login-submit') and username and pswd:
        print(username, pswd)
        if check_user(username, pswd):
            dic = {
                'LinkRef': 'AL1000',
                'DataQuality': None,
                'fromDate': None,
                'toDate': None
            }
            return flask.render_template("charts.html", filter=json.dumps(dic))
        else:
            redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
```

+ 获取前端请求的参数并且渲染页面的功能如下：

```
@app.route("/filter_chart1", methods=['post', 'get'])
def filter_chart1():
    linkref = request.form.get('LinkRef', "AL1000")
    DataQuality = request.form.get('DataQuality', None)
    fromdate = request.form.get('fromDate', None)
    todate = request.form.get('toDate', None)
    dic = {
        'LinkRef': linkref,
        'DataQuality': DataQuality,
        'fromDate': fromdate,
        'toDate': todate
    }
    return flask.render_template("charts.html", filter=json.dumps(dic))
```

因为D3.js已经实现了filter的功能，所以这里的筛选是返回一个json数据，并且在前台绘图的时候让D3.js使用这个json来进行数据筛选，这里默认是显示id为AL1000的这条线路上的交通数据。

+ 前端筛选数据的功能如下：

```
d3.csv("./static/MAR15.csv", type, function(data) {
        
        if (filter['LinkRef']){
            data = data.filter(function(row) {
                return row['LinkRef'] == filter['LinkRef'];
             })
        };

        if (filter['DataQuality']){
            data = data.filter(function(row) {
                return row['DataQuality'] == filter['DataQuality'];
             })
        }; 

        if (filter['toDate']){
            data = data.filter(function(row) {
                return row['Date'] < filter['toDate'];
             })
        };
        
        if (filter['fromDate']){
            data = data.filter(function(row) {
                return row['Date'] > filter['fromDate'];
             })
        };
```


这里用到的filter就是从后端返回的json数据，在渲染html文件的时候这个数据被写在了js代码里，如下所示：


```
var filter = {{filter|tojson}};
    filter = JSON.parse(filter);
```


## 3. 展示

这个系统实现的功能包括数据范围的筛选，散点图的缩放等，展示效果如下：

![img](image/login.png)


![img](image/flowchart.png)


![img](image/filterflowchart.png)


![img](image/parallelchart.png)


![img](image/filterparallelchart.png)

![img](image/scatter.png)

![img](image/table.png)

## 4. 问题

1.为什么没有用数据库保存数据，并且通过SQL语句控制数据的显示范围？

这是因为数据量比较大把104万条数据全部存入数据库需要很长时间，一开始的设计是有一个文件上传功能，并且在上传文件之后会将文件中的数据全部存入SQLite数据库，之后的数据查询都会通过SQL语句或者Flask中的ORM与数据库交互。但是在实际实现的时候，发现这个数据文件存入数据库需要很长时间。
用ORM的时候尝试了两种方式：
- 第一种是循环读取文件数据，循环次数就是数据条数，每次循环都会实例化一个新的实例，并且加入ORM的session中，并且在循环内提交这个session，这种情况需要很长的时间，因为循环里每一次的循环都要维护一个session的对象，并且在这次循环里commit这个session，下一次循环又维护一个全新的session，这样会消耗非常多的时间，所以不可行。
- 第二种方式也是循环读取数据，循环次数就是数据条数，每次循环都会实例化一个新的实例，并且加入ORM的session中，但是在循环内不提交这个session，等所有循环结束之后提交这个session，这样全程就只维护了一个session对象，但是这也会造成一个问题session.add()只是注册了事务但是并没有提交事务，没有与数据库交互，数据保存在计算机内存中，当调用session.flush()时才会将一系列操作传递给数据库，数据库将它们作为挂起的操作维护在事务中。 这些更改目前也不会永久持久地保存到磁盘上，也不会在数据库收到当前事务的提交之前对其他事务可见，只有在调用session.commit()提交了当前事务，这些更改才是永久保存到磁盘上并且对其他事务可见的。用这种方式，在我的电脑上测试的时候运行到中途就提示内存不够并且退出了程序，因为session.add()之后数据保存在计算机内存中，内存没有足够的空间所以会提示错误并退出。

在之后的实验中使用了五种方式进行测试，测试SQLite数据库写入10万条数据所用的时间，测试用到的写数据库方式包括sqlalchemy\_orm，sqlalchemy\_orm\_bulk\_save\_objects，sqlalchemy\_orm\_bulk\_insert，sqlalchemy\_core和原生的SQLite3中的insert语句。详细的测试代码见test.py文件，测试结果如下图所示：

![img](image/test_sqlalchemy.png)

可以看到最慢的方式是用普通的ORM，插入10万条数据花费了439秒，最快的方式是原生的SQL语句与SQLite3交互，但是即使是最快的方式，也要用15秒的时间。综上可见，把所有的数据都存入数据库花费的时间很多，而且D3.js提供了数据筛选的功能，因此就没有把数据存入数据库。

2.数据文件中的时间是分两列显示的，一列显示日期，一列显示的是时间戳，时间戳的间隔是15分钟，那么如何在画流量图的时候让横轴显示的是连续递增的精确到分钟的时间？

这里将时间戳转换成时间点的做法是：
- 时间戳间隔是15分钟，所以用时间戳乘以15算出总分钟数
- 总分钟数除以60，商记为h
- 总分钟数除以60，余数记为m
- 对于h和m，不足两位的在数字左边补0，使其补足两位
- 将数据中的日期和时间结合，组成一个包括日期和时间的字符串，类似于“2017/08/01 15:30”，将这个字符串记作b
- 将b格式化成时间对象，并且赋值给数据中原来的Date属性（原来的Date属性只包括了日期，timePeriod属性表示时间戳）

具体实现的代码如下：
```
var format = d3.timeParse("%m/%d/%y %H:%M");
function pad(num, n) {
        return Array(n > num ? (n - ('' + num).length + 1) : 0).join(0) + num;
    }
function type(d) {
        var m = (d.TimePeriod * 15) % 60;   //计算分钟
        var h = parseInt((d.TimePeriod * 15) / 60); //计算小时
        var b = d.Date + ' ' + pad(h, 2) + ':' + pad(m, 2); // 日期加时间的字符串
        d.date = format(b); // 将格式化后返回的时间对象赋值给date属性
        d.flow = +d.Flow;
        return d;
    }
```