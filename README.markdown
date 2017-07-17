# Traffic data analysis and Visualization

## 1. 介绍
这是一个用Flask实现简单粗糙的后端，用D3.js和Bootstrap实现前端的交通大数据显示系统。测试的数据源为csv格式，包含104万条交通数据。后端实现的功能包括用户的登陆和注册，以及数据显示范围的筛选。前端实现的功能是对交通数据的各种图表显示，其中包括交通流量图、平行坐标图、散点图以及原始数据表格的展示。

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