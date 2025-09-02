from jodellSdk.jodellSdkDemo import RgClawControl
import time

clawControl = RgClawControl()

# 打开搜索
comList = clawControl.searchCom()
flag = clawControl.serialOperation(comList[0], 115200, 1)
print(f"建立连接: {flag}")

flag = clawControl.enableClamp(9, True) # 去使能，id为9的夹爪
print(f"使能: {flag}")
time.sleep(3)

flag = clawControl.runWithoutParam(9, 1)
print(f"无参模式,夹爪开: {flag}")

for i in range(10):
    pos = clawControl.getClampCurrentLocation(9)
    speed = clawControl.getClampCurrentSpeed(9)
    torque = clawControl.getClampCurrentTorque(9)
    status = clawControl.getClampCurrentState(9)
    print(f"状态: {status}")
    print(f"位置: {pos}, 速度: {speed}, 力矩: {torque}")
    time.sleep(0.2)

flag = clawControl.enableClamp(9, False) # 去使能，id为9的夹爪
print(f"去使能: {flag}")
time.sleep(3)