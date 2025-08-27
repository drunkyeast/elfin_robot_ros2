# 可以只看这个文档。ros2环境安装的时候看README_cn.md（大族的文档）
## 相比于大族官方的代码仓库（fix cartPath这个commit）的修改
陈峻威@华沿机器人修改部分：修改内容主要是elfin_ethercat_driver/下面的几个文件。大概逻辑就是，新的机箱增加了从节点（slave）然后修改一些数字，如1，2，3改成2，3，4。参数4改成5这样的修改。这内容是大族机械臂和机箱相关的，不用太care。
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


## ROS2环境机械臂启动步骤如下（环境安装好后直接从这儿开始）
1. 用示教器正常启动，机箱网线是连接ROBOT接口的, 然后示教器上面断电，选择右下角的“模拟“模式，然后重新上电，但不要初始化和使能。
2. 拔掉ROBOT接口的网线，用网线对接插口来延长网线, 插入linux主机。
3. linux主机按照README_cn.md中最下面的四条命令(拷贝如下)，开四个终端依次执行。
```sh
# 终端1
sudo chrt 10 bash
ros2 launch elfin5_ros2_moveit2 elfin5_moveit.launch.py

# 终端2
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
5. 第二个终端启动rviz，用法在文档中有。在完成第后两步后，在rviz上调整位置，然后plan 和 excute也能让机械臂动。
6. 第三个终端+第四个终端是后台程序和控制面板。然后用控制面板点击servo on（使能），然后就可以控制机械臂了。但是我长按移动有时会出问题卡死，不得不回到第一个终端步骤。所以建议不要长按，点动，幅度小一点。
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
cd /home/ubuntu/ros2_ws/src/elfin_robot_ros2_modified-main
python3 mouseScripts/gripper_button_control.py      # 启动夹爪的控制脚本

##有问题时，测试，重新插拔usb
/home/ubuntu/ros2_ws/src/elfin_robot_ros2_modified-main/claw_junduo# python3 test.py 

# 终端4 机械臂末端
sudo su
cd /home/ubuntu/ros2_ws/src/elfin_robot_ros2_modified-main
python3 mouseScripts/version1.py    # 启动机械臂末端的控制脚本
```
