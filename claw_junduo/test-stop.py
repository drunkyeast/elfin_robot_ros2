from jodellSdk.jodellSdkDemo import RgClawControl
import time

# 建立连接
clawControl = RgClawControl()
comList = clawControl.searchCom()
flag = clawControl.serialOperation(comList[0], 115200, 1)

flag = clawControl.enableClamp(9, True) # 去使能id为9的夹爪
print(f"使能: {flag}")
time.sleep(3)

flag = clawControl.runWithoutParam(9, 2)
print(f"无参模式,夹爪合: {flag}")
time.sleep(3)
flag = clawControl.runWithoutParam(9, 1)
print(f"无参模式,夹爪开: {flag}")

for i in range(10):
    # flag = clawControl.stopClaw(9)
    # print(f"停止: {flag}")
    flag = clawControl.enableClamp(9, False) # 去使能id为9的夹爪
    print(f"使能: {flag}")
    time.sleep(0.1)

