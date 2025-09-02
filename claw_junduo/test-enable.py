from jodellSdk.jodellSdkDemo import RgClawControl
import time

clawControl = RgClawControl()

# 打开搜索
comList = clawControl.searchCom()
flag = clawControl.serialOperation(comList[0], 115200, 1)
print(f"建立连接: {flag}")

for i in range(3):
    print(f"循环第{i}次，每次使能3秒，去使能3秒")
    flag = clawControl.enableClamp(9, True) # 去使能id为9的夹爪
    print(f"使能: {flag}")
    time.sleep(3)
    flag = clawControl.enableClamp(9, False) # 去使能id为9的夹爪
    print(f"去使能: {flag}")
    time.sleep(3)

