# 南理工紫金学院校园网认证工具

> 免责声明：该工具只提供校园网的辅助认证功能，旨在实现设备自动认证上网，不提供绕开校园网认证直接上网的服务。

## 前言

相信你在使用校园网的过程中一定遇到了这些情况：

> 为什么我才在宿舍认证过，到教学楼之后又要重新认证了？
> 为什么我在宿舍下载资源的设备又被挤掉线了？

所以，在`deepseek`的友情帮助下，我写了以下脚本，并希望他能造福学弟学妹（如果能造福到学长学姐那更好[doge]）。
那话不多说，我来介绍一下这个脚本怎么使用吧！

## 使用方法：

1. 运行`.exe`文件，会在当前位置生成`zj_account.ini`的一个配置文件  
   <img width="1687" height="945" alt="image" src="https://github.com/user-attachments/assets/31cdae70-5a89-49b5-8cf4-1e1ed6fc714c" />
   > 注：更新后`config.ini`已被重命名为`zj_account.ini`
2. 打开`zj_account.ini`文件，按照文件中的提示输入自己的校园网账号信息  
   <img width="813" height="1098" alt="image" src="https://github.com/user-attachments/assets/fa4d4723-5c00-4a42-8f19-07e37aa42b6e" />
3. 再次运行`.exe`文件即可正常使用

### 进阶设置：

#### 自动认证脚本：

与其他版本不同，为了能在后台监听网络是否连接不被误关，隐藏了该版本的控制台，引入了日志，所以双击后没有出现窗口是正常的。

> 怎么确认脚本是否在运行呢？
> - 首次运行会生成一个`zj_network.log`的日志文件，可以查看日志中是否有运行的记录  
>   <img width="811" height="1096" alt="image" src="https://github.com/user-attachments/assets/0f6e8086-04e2-4877-b676-6ab648abb9e7" />
> - 当然，你也可以在`任务管理器`中查看脚本是否在运行  
>   <img width="569" height="433" alt="image" src="https://github.com/user-attachments/assets/5c83fbaa-4752-433b-8457-4e9cefd8417d" />

> 怎么关闭脚本呢？
> - 在`任务管理器`中右键并选择结束任务  
>   <img width="1139" height="859" alt="image" src="https://github.com/user-attachments/assets/5bc83ff7-9e8c-49fa-b174-268714dc6866" />

#### 开机自动认证

这是整个脚本画龙点睛的关键一步，完成这步你的校园网体验会得到很好的优化。
接下来我会分不同方法进行设置。

##### Windows

1. 右键`开始菜单`，打开`计算机管理`  
   <img width="101" height="475" alt="image" src="https://github.com/user-attachments/assets/8dffc736-2509-41ca-b8cc-d9a775e09763" />
2. 在弹出的界面中找到`系统工具 > 任务计划程序`，单击`创建任务`  
   <img width="734" height="526" alt="image" src="https://github.com/user-attachments/assets/848d3d62-deff-406d-9da8-28bd6fa3f57e" />
3. `常规`里给任务随便起一个名称，**一定要勾选`使用最高权限运行`！**  
   <img width="736" height="526" alt="image" src="https://github.com/user-attachments/assets/52e7b0ef-029a-4f41-b5bf-b01c839a4cf5" />
   > *因为开机自启动的路径默认在`C:\Windows\System32`中，在该文件夹下的读写操作都需要使用管理员权限*
4. 单击`触发器`，`新建`，将开始任务改为`登录时`，`确定`  
   <img width="734" height="527" alt="image" src="https://github.com/user-attachments/assets/b993adf0-e2b4-4236-a5be-59655f028215" />
5. 单击`操作`、`新建`，操作就选`启用程序`，单击`浏览`，选择`.exe`文件，`确定`  
   <img width="734" height="527" alt="image" src="https://github.com/user-attachments/assets/d6cb6b1c-be5c-4969-b25e-b679fbd5a5a1" />
6. `条件`中，如果你用的是笔记本，可以取消勾选`只有在计算机使用交流电源时才启动此任务`，其他可以不用改，`确定`  
   <img width="733" height="526" alt="image" src="https://github.com/user-attachments/assets/d67c4614-4e31-449a-974b-27e5ddad58fa" />
7. 往下找到刚才创建的任务，双击  
   <img width="1469" height="1054" alt="image" src="https://github.com/user-attachments/assets/a2d690bb-a1b9-438d-9cdb-464d7c91a117" />
8. 单机右边的`运行`  
   <img width="734" height="526" alt="image" src="https://github.com/user-attachments/assets/99f512ce-6907-49bf-887c-acadae85a30a" />
9. 打开`文件资源管理器`，找到`C:\Windows\System32\config.ini`文件并打开，按照文件中的提示输入自己的校园网账号信息  
    > **目前的该文件夹下应该没有同名文件，如果有，建议不要强行覆盖**
10. 再次重复步骤7、8即可正常使用

##### Docker *[Docker项目地址][]*

如果你的系统上有Docker的话，使用Docker绝对是你的不二之选。
目前已适配amd64和arm64系统，安装了`vim`编辑器
拉取镜像：
```bash
docker pull yunyuanweigui06/zj_auto_login
```
后续使用可以先自己暂时摸索一下，后续我会完善教程。

[Docker项目地址]: https://hub.docker.com/repository/docker/yunyuanweigui06/zj_auto_login
