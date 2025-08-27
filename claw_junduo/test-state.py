from jodellSdk.jodellSdkDemo import RgClawControl
import time

clawControl = RgClawControl()

# 打开搜索
comList = clawControl.searchCom()
flag = clawControl.serialOperation(comList[0], 115200, 1)
print(f"建立连接: {flag}")

flag = clawControl.runWithoutParam(9, 2)
print(f"无参模式,夹爪合: {flag}")
time.sleep(3)
flag = clawControl.runWithoutParam(9, 1)
print(f"无参模式,夹爪开: {flag}")

for i in range(5):
    pos = clawControl.getClampCurrentLocation(9)
    speed = clawControl.getClampCurrentSpeed(9)
    torque = clawControl.getClampCurrentTorque(9)
    status = clawControl.getClampCurrentState(9)
    print(f"状态: {status}")
    print(f"位置: {pos}, 速度: {speed}, 力矩: {torque}")
    time.sleep(0.5)