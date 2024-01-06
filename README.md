# 项目介绍：[Embedded-Project项目介绍](https://blog.csdn.net/wryf602/article/details/135431606)

# Server后端项目
系统后端项目，基于django实现
后端环境：python3、django、sqlite3

## 后端启动
直接采用命令行`python manage.py runserver` 或 pycharm配置启动[Pycharm 配置运行 Django 项目](https://zhuanlan.zhihu.com/p/246400570)

## 连接数据库

```bash
python manage.py makemigrations
python manage.py migrate
```

## 启动时可能遇到的问题

 - `No module named 'corsheaders'`
解决方法：`pip install django-cors-headers` 

 - `No module named 'numpy'`
解决方法：`pip install numpy`

 - `No module named 'graphviz'`
解决方法：`pip install graphviz`

 - `No module named 'untangle'`
  解决方法：`pip install untangle`

## 架构介绍
项目包含以下主要文件和文件夹：
 - **background(generation):**  项目的主要工程代码
 **-models.py:** 定义数据模型
 **-urls.py:** 处理 URL 映射
 **-views.py:** 执行业务逻辑
 - **server:** 连接配置
**-settings.py:**  Django 项目的主要设置文件，其中包含了许多配置选项，例如数据库设置、静态文件设置、中间件配置等。在这里，你可以设置许多与服务器相关的选项。

出现`Starting development server at http://localhost:xxxx/`代表启动成功
![后端启动成功](https://img-blog.csdnimg.cn/direct/7da9aa32f45547da8e477522e40feb05.png)

# web前端项目
系统前端项目，基于vue实现
环境配置：npm、node、vue-cli

## 前端启动

 1. `npm install` 安装配置
 2. `npm server` 启动项目

![show npm scripts](https://img-blog.csdnimg.cn/direct/1462e265d95b4cc8ab0ee7cf00fec219.png)
## 启动时可能遇到的问题

 - `node-sass`已废弃
解决方法：使用sass替代，    `"sass": "^1.26.5"`
 - eslint严格限制代码规范
 解决方法：移除    ` 'no-unused-vars': 'off'`

## 架构介绍
一个 Vue 项目通常包含以下主要文件和文件夹：
 - **src/:** 包含项目的源代码。
**assets/:** 存放静态资源文件，如图片、样式表等。
**components/:** 存放 Vue 组件。
**-views/:** 存放页面级别的组件。
**-router/:** 存放路由配置文件。
**-store/:** 存放 Vuex 状态管理相关文件。

 - 与后端连接api设置
Api.vue下修改`const Global_Api = 'http://127.0.0.1:4096'`

出现`app running at`代表前端启动成功

```python
  App running at:
  - Local:   http://localhost:xxxx/
  - Network: http:
```

![前端启动成功](https://img-blog.csdnimg.cn/direct/5cb5e449da96440c878b966d4b6e6897.png)

# 前后端分离开发流程
前后端可分别开发，后端完成代码接口提供给前端调用即可

 1. 后端在 myapp/views.py 中编写一个简单的视图
```python
from django.http import JsonResponse

def get_data(request):
    data = {'message': 'Hello from Django!'}
    return JsonResponse(data)
    
```
 2. 后端urls.py 中配置该视图的 URL：
 

```python
from django.urls import path
from myapp.views import get_data

urlpatterns = [
    path('api/get_data/', get_data, name='get_data'),
    # 其他 URL 配置...
]

```
即可得到该功能接口`http://localhost:xxxx/api/get_data/`，提供给前端使用

 3. 前端编写一个简单的组件hello.vue：
```html
<template>
  <div id="app">
    <h1>{{ message }}</h1>
  </div>
</template>

<script>
export default {
  data() {
    return {
      message: 'Hello from Vue!',
    };
  },
  mounted() {
    // 使用后端接口
    this.$axios.get('http://127.0.0.1:xxxx/api/get_data/')
      .then(response => {
        this.message = response.data.message;
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

h1 {
  font-size: 2em;
  margin-bottom: 20px;
}
</style>

```
