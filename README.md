# 可以只看这个文档。ros2环境安装的时候看README_cn.md（大族的文档）
## 快速构建代码，安装本软件包
关于代码空间的命名，建议命名为`ros2_ws`，而不是`catkin_ws`。
```sh
mkdir -p ~/ros2_ws/src && cd ~/ros2_ws/src
git clone https://github.com/drunkyeast/elfin_robot_ros2.git
cd ..
colcon build
source install/setup.bash
```
不要创建太多工作空间并放入.bashrc中，容易污染环境变量。

## 相比于大族官方的代码仓库（fix cartPath这个commit）的修改
陈峻威@华沿机器人修改部分：修改内容主要是elfin_ethercat_driver/下面的几个文件。因为新的机箱增加了从节点（slave）。这内容是大族机械臂和机箱相关的，不用care。

然后我增加了`claw_junduo/`,`mouseScripts/`,`README.md`，删除了原来的英文版的`README.md`,修改了`README_cn.md`的一些配置文件的内容，如原点参数，网卡，以及把默认的elfin3改成了elfin5。但其实逻辑上夹爪`claw_junduo/`应该是与机械臂无关的，为了方便我就放在一起了。


## 环境安装
#### 一、 ros2环境安装参考README_cn.md
#### 二、 3d鼠标驱动以及3d鼠标ros2包安装:`sudo apt install spacenavd` 以及 `sudo apt install ros-foxy-spacenav`。
#### 三、 3d鼠标驱动编译安装:因为apt安装的spacenavd版本太旧了。需要编译安装新一点的驱动。[参考这篇文档吧，驱动不要设置开机自启，我是把重要部分已经提取如下了](https://blogs.seecsdn.cn/online/2025-07-24/fca79ada30eb64ca487b10c4ba5e1f60.html) 。下面两个项目spacenavd是驱动，libspnav是用于测试。
```sh
git clone https://github.com/FreeSpacenav/spacenavd.git
cd spacenavd
./configure
make
sudo make install # 会安装到/usr/local/bin/spacenavd下面
```
```sh
git clone https://github.com/FreeSpacenav/libspnav.git
cd libspnav
./configure
make
sudo make install

# 然后到这里面进行测试驱动是否正常
cd /home/ubuntu/zq/about_spacemouse/libspnav/examples/simple
make
./simple_af_unix

# 图形化测试驱动
/home/ubuntu/zq/about_spacemouse/libspnav/examples/cube
./cube 
```
#### 四、钧舵夹爪的pip包
`claw_junduo/`下面, `pip install JodellTool-0.1.5-py3-none-any.whl`
`claw_junduo/`下面还有一些根据文档的测试脚本。
#### 五、 ~/.bashrc环境变量 root和ubuntu用户下都要有。
```sh
source /opt/ros/foxy/setup.bash                                     # ros2环境变量
source /home/ubuntu/ros2_ws/install/setup.bash                      # 编译安装的环境变量，注意路径
export LD_LIBRARY_PATH=/opt/ros/foxy/lib/spacenav:$LD_LIBRARY_PATH  # 编译安装的鼠标驱动环境变量
```


## ROS2环境机械臂启动步骤如下（环境安装好，代码编译完后直接从这儿开始）
1. 用示教器正常启动，机箱网线是连接ROBOT接口的, 然后示教器上面断电，选择右下角的“模拟“模式，然后重新上电，但不要初始化和使能。
2. 拔掉ROBOT接口的网线，用网线对接插口来延长网线, 插入linux主机。
3. linux主机按照README_cn.md中最下面的四条命令(拷贝如下)，开四个终端依次执行。
```sh
# 终端1
sudo chrt 10 bash
ros2 launch elfin5_ros2_moveit2 elfin5_moveit.launch.py

# 终端2 第一个终端启动后，稍等一会儿再启动，注意启动后rviz界面中机械臂姿态要与实际一致。
sudo su
ros2 launch elfin5_ros2_moveit2 elfin5_moveit_rviz.launch.py

# 终端3
sudo su
ros2 launch elfin5_ros2_moveit2 elfin5_basic_api.launch.py

# 终端4
sudo su
ros2 launch elfin_basic_api elfin_gui.launch.py
```
4. 第一个终端没有ethercat报错应该就没问题。否则接线出问题了。关于ethercat我的简单理解是工业相关的ether网协议（链路层），与平时用的ether网协议还不同。并且插上后，linux主机是ping不通机械臂机箱的。而机械臂机箱其他网口如enp3s0、enp4s0在保证两边网卡在同一网段下是能ping通的。
5. 第二个终端启动rviz，注意rviz界面中机械臂姿态要与实际姿态一致。在启动完终端3和4后，可以在rviz上调整位置，银色是实际位置，黄色是目标位置，然后plan 和 excute也能让机械臂动。
6. 第三个终端+第四个终端是后台程序和控制面板。然后用控制面板点击servo on（使能），然后就可以控制机械臂了。长按太久容易出问题，所以建议点动，幅度小一点。
7. 关闭时流程：控制面板先servo off（去使能），然后再去示教器上面断电源，示教器上面右上角关闭系统。最后把网线恢复最初模样。

## 用3d鼠标操控机械臂移动（因为前面都是在sudo su环境下启动，下面也要先sudo su再执行, 如果是仿真环境就不需要sudo su）
```sh
# 终端1 启动编译安装的spacenavd，对应3D鼠标
sudo systemctl stop spacenavd       # 因为apt安装的spacenavd驱动版本太旧了。
sudo su
sudo /usr/local/bin/spacenavd -d    # 启动编译安装的spacenavd， 

# 终端2 启动ros2
sudo su
ros2 run spacenav spacenav_node     # 启动ros2，没有输出是正常的

# 终端3  夹爪
sudo su
cd /home/ubuntu/ros2_ws/src/elfin_robot_ros2        # 注意修改路径
python3 mouseScripts/gripper_button_control.py      # 启动夹爪的控制脚本
# 有问题时，重新插拔usb，且claw_junduo/下面有测试脚本

# 终端4 机械臂末端
sudo su
cd /home/ubuntu/ros2_ws/src/elfin_robot_ros2        # 注意修改路径
python3 mouseScripts/version2.py    # 启动机械臂末端的控制脚本 version2调参后的，比version1更好用。
```
## 关于mouseScripts，以及调参
```python
# 控制参数
self.deadzone = 0.03      # 死区阈值（降低以提高灵敏度）
self.last_call_time = 0.0   # 上次调用时间
self.min_interval = 0.05    # 最小调用间隔50ms（提高响应性）
self.last_input_time = 0.0  # 上次有输入的时间
self.stop_timeout = 0.1     # 停止超时时间100ms
self.is_moving = False      # 是否正在运动

# 参数缓存，避免重复调用相同参数的服务
self.last_command_data = None    # 上次发送的指令数据
self.command_repeat_count = 0    # 相同指令的重复次数
self.max_repeat_count = 1        # 最大允许重复次数（避免完全不发送）
```
主要是deadzone调整灵敏度，stop_timeout松开鼠标后多久后停止运动，min_interval是命令发送的帧率0.05对应20帧。max_repeat_count不需要了，就设置成1就好，是之前处理bug的残留。