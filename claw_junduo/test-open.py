from jodellSdk.jodellSdkDemo import RgClawControl
import time

clawControl = RgClawControl()

# 打开搜索
comList = clawControl.searchCom()
flag = clawControl.serialOperation(comList[0], 115200, 1)
print(f"建立连接: {flag}")

flag = clawControl.enableClamp(9, True) # 去使能id为9的夹爪
print(f"使能: {flag}")
time.sleep(3)
flag = clawControl.runWithoutParam(9, 1) # 1表示夹爪开, 2表示夹爪合。
print(f"无参模式,夹爪开: {flag}")
time.sleep(3)
flag = clawControl.enableClamp(9, False) # 去使能id为9的夹爪
print(f"去使能: {flag}")
time.sleep(3)

