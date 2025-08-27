from jodellSdk.jodellSdkDemo import RgClawControl
import time

clawControl = RgClawControl()

# 打开搜索
comList = clawControl.searchCom()
flag = clawControl.serialOperation(comList[0], 115200, 1)
print(f"建立连接: {flag}")


# 1表示夹爪开, 2表示夹爪合, 运行就能控制夹爪开合
flag = clawControl.runWithoutParam(9, 1)
print(f"无参模式,夹爪开: {flag}")
time.sleep(3)
flag = clawControl.runWithoutParam(9, 2)
print(f"无参模式,夹爪合: {flag}")
time.sleep(3)
flag = clawControl.runWithParam(9, 20, 100, 100)
print(f"有参模式,夹爪开, 位置20, 速度100, 力矩100: {flag}")
time.sleep(3)
flag = clawControl.runWithParam(9, 200, 100, 100)
print(f"有参模式,夹爪合, 位置200, 速度100, 力矩100: {flag}")
time.sleep(3)

