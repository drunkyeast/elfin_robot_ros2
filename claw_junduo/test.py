from jodellSdk.jodellSdkDemo import RgClawControl
import time

clawControl = RgClawControl()

# 打开搜索
comList = clawControl.searchCom()
flag = clawControl.serialOperation(comList[0], 115200, 1)
print(f"建立连接: {flag}")

# 上使能时，夹爪会自动开合一次，如果夹爪已经开了，那么就闭合。如果已经上使能了，再上使能就无效。官方文档都没说这些。
flag = clawControl.enableClamp(9, True) # 上使能，id为9的夹爪
print(f"使能: {flag}")
time.sleep(3)

flag = clawControl.runWithoutParam(9, 1)
print(f"无参模式,夹爪开: {flag}")
time.sleep(3)
flag = clawControl.runWithoutParam(9, 2)
print(f"无参模式,夹爪合: {flag}")
time.sleep(3)
flag = clawControl.runWithParam(9, 20, 50, 100)
print(f"有参模式,夹爪开, 位置20, 速度50, 力矩100: {flag}")
time.sleep(3)
flag = clawControl.runWithParam(9, 200, 50, 100)
print(f"有参模式,夹爪合, 位置200, 速度50, 力矩100: {flag}")
time.sleep(3)

# 结束后要去使能，标准一点，不然会影响测试逻辑。这就是走过的坑啊。
flag = clawControl.enableClamp(9, False) # 去使能，id为9的夹爪
print(f"去使能: {flag}")
time.sleep(3)