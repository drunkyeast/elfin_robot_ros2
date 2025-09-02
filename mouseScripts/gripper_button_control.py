#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
import time
import sys
import os

from jodellSdk.jodellSdkDemo import RgClawControl

class GripperButtonControl(Node):
    def __init__(self):
        super().__init__('gripper_button_control')
        
        # 初始化夹爪控制
        self.init_gripper()
        
        # 订阅SpaceMouse按键
        self.joy_subscriber = self.create_subscription(
            Joy,
            '/spacenav/joy',
            self.joy_callback,
            10
        )
        
        # 按键状态跟踪
        self.last_buttons = None
        self.gripper_state = None  # None=未知, True=开, False=合
        
        self.get_logger().info('=== SpaceMouse夹爪控制节点已启动 ===')
        print("🎮 控制说明:")
        print("  按键1 (左键)  → 夹爪开")
        print("  按键2 (右键)  → 夹爪合")
        print("=" * 50)
        
    def init_gripper(self):
        """初始化夹爪连接"""
        try:
            self.clawControl = RgClawControl()
            
            # 搜索串口并建立连接
            com_list = self.clawControl.searchCom()
            if not com_list:
                self.get_logger().error("❌ 未找到夹爪设备")
                raise Exception("未找到夹爪设备")
                
            flag = self.clawControl.serialOperation(com_list[0], 115200, 1)
            if flag:
                self.get_logger().info(f"✅ 夹爪连接成功: {com_list[0]}")
                # 先去使能，再上使能，避免潜在bug。
                flag = self.clawControl.enableClamp(9, False) # 去使能，id为9的夹爪
                self.get_logger().info(f"去使能: {flag}")
                time.sleep(0.5)
                flag = self.clawControl.enableClamp(9, True) # 上使能，id为9的夹爪
                self.get_logger().info(f"使能: {flag}")
                self.get_logger().info(f"第一次上使能成功的话，夹爪会开合一次，等待3秒")
                time.sleep(3)
            else:
                self.get_logger().error("❌ 夹爪连接失败")
                raise Exception("夹爪连接失败")
                
        except Exception as e:
            self.get_logger().error(f"夹爪初始化失败: {e}")
            sys.exit(1)
    
    def joy_callback(self, msg):
        """处理SpaceMouse按键输入"""
        if len(msg.buttons) == 0:
            return
            
        # 创建固定长度的按键数组
        current_buttons = [0, 0]
        if len(msg.buttons) >= 1:
            current_buttons[0] = msg.buttons[0]
        if len(msg.buttons) >= 2:
            current_buttons[1] = msg.buttons[1]
        
        # 只在按键状态改变时处理
        if self.last_buttons != current_buttons:
            # 检测按键按下（从0变为1）
            if self.last_buttons is not None:
                # 按键1按下 - 夹爪开
                if current_buttons[0] and not self.last_buttons[0]:
                    self.gripper_open()
                    
                # 按键2按下 - 夹爪合
                if current_buttons[1] and not self.last_buttons[1]:
                    self.gripper_close()
            
            self.last_buttons = current_buttons
    
    def gripper_open(self):
        """夹爪开"""
        try:
            timestamp = time.strftime("%H:%M:%S")
            print(f"[{timestamp}] 🖐️  执行夹爪开...")
            
            # 使用无参模式：1表示夹爪开
            flag = self.clawControl.runWithoutParam(9, 1)
            # 使用有参模式，更细粒的控制。开的时候力矩无所谓
            # flag = self.clawControl.runWithParam(9, 20, 50, 100)
            # self.get_logger().info(f"有参模式,夹爪开, 位置20, 速度50, 力矩100: {flag}")
            
            if flag:
                self.gripper_state = True
                self.get_logger().info("✅ 夹爪开指令发送成功")
                print("  → 夹爪正在打开...")
            else:
                self.get_logger().warn("❌ 夹爪开指令发送失败")
                
        except Exception as e:
            self.get_logger().error(f"夹爪开操作异常: {e}")
    
    def gripper_close(self):
        """夹爪合"""
        try:
            timestamp = time.strftime("%H:%M:%S")
            print(f"[{timestamp}] ✊ 执行夹爪合...")
            
            # 使用无参模式：2表示夹爪合
            # flag = self.clawControl.runWithoutParam(9, 2)
            # 使用有参模式, 主要是力矩参数, 设为50差不多是最小了。参数范围都是0~255。
            flag = self.clawControl.runWithParam(9, 255, 50, 50)
            self.get_logger().info(f"有参模式,夹爪合, 位置255, 速度50, 力矩50: {flag}")
            
            if flag:
                self.gripper_state = False
                self.get_logger().info("✅ 夹爪合指令发送成功")
                print("  → 夹爪正在闭合...")
            else:
                self.get_logger().warn("❌ 夹爪合指令发送失败")
                
        except Exception as e:
            self.get_logger().error(f"夹爪合操作异常: {e}")
    
    def get_gripper_status(self):
        """获取夹爪状态（可选功能）"""
        try:
            pos = self.clawControl.getClampCurrentLocation(9)
            speed = self.clawControl.getClampCurrentSpeed(9)
            torque = self.clawControl.getClampCurrentTorque(9)
            status = self.clawControl.getClampCurrentState(9)
            return pos, speed, torque, status
        except Exception as e:
            self.get_logger().warn(f"获取夹爪状态失败: {e}")
            return None, None, None, None

def main():
    rclpy.init()
    
    try:
        node = GripperButtonControl()
        
        print("\n🚀 开始监听SpaceMouse按键...")
        print("💡 提示：按住按键不会重复执行，只在按下瞬间触发")
        print("\n按 Ctrl+C 退出程序\n")
        
        rclpy.spin(node)
        
    except KeyboardInterrupt:
        print('\n👋 收到停止信号，退出程序...')
    except Exception as e:
        print(f'\n❌ 程序异常: {e}')
    finally:
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()
