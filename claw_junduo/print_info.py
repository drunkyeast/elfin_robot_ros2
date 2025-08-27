from jodellSdk.jodellSdkDemo import RgClawControl

clawControl = RgClawControl()

# 打开搜索, 建立连接, 必须的.
comList = clawControl.searchCom()
flag = clawControl.serialOperation(comList[0], 115200, 1)
print(flag)

# 读写数据
data = clawControl.readRegisterData(9, 4, 2000, 2)
print(data)
flag = clawControl.writeDataToRegister(9, 1000, [1, 2])
data = clawControl.readRegisterData(9, 4, 1000, 2)
print(data)

# 获取温度
temp = clawControl.getDeviceCurrentTemperature(9)
print(f"温度: {temp}度")
voltage = clawControl.getDeviceCurrentVoltage(9)
print(f"电压: {voltage}V")
softwareVersion = clawControl.readSoftwareVersion(9)
print(f"软件版本: {softwareVersion}")
slaveIdList = clawControl.scanSlaveId(1, 10)
print(f"扫描从机ID列表: {slaveIdList}")
# 关于ID的修改和波特率的修改见文档, 这儿就不写了.