# T2CAN Universal Unlock (特斯拉双路 CAN 增强工程)

> ⚠️ **研发与测试安全声明**  
> 本项目涉及特斯拉汽车 CAN 总线逆向与信号注入研究。仅供在受控台架、实验室或个人封闭测试环境下进行学习与技术验证。严禁在公共道路或未经安全评估的场景下盲目依赖辅助驾驶注入。使用者须自行对接线安装、硬件修改及相关法规合规性负责。

---

## 📌 项目定位与功能概览

本项目基于开源固件 **T2CAN Universal Unlock (v3.29.1)** 搭建了完整的硬件选型、PCB 改造、PlatformIO 工程化构建与实车适配体系。

### 核心功能矩阵：
1. **免手扶方向盘提醒消除 (NAG Killer)**：
   - **Mode H Rev.4 拟人微扭矩注入**（车速为 0 km/h 自动静止暂停，驾驶员主动打方向瞬时避让）；
   - **AP 滚轮按键仿真**（识别 DAS 0x24A / 0x399 视觉告警信号，自动模拟滚轮按压消除提示）。
2. **欧盟法规限制绕过 (EU Unlock)**：
   - 绕过 ECE R79 严苛限制，解除过弯横向加速度限制；
   - 智能召唤（Smart Summon）距离由 6 米扩展至 **±85 米**；
   - 打灯变道超时取消解除、分叉路口变道增强。
3. **高级增强辅助驾驶自动打灯 (Advanced EAP)**：
   - 自动检测 NOA 变道指令并模拟转向灯激活，支持屏幕、开门键、S3XY 按键随时取消。
4. **S3XY 蓝牙实体按键无缝支持**：
   - 支持最多 3 枚 S3XY 按键免网关直连，实现实体按键打灯、变道取消与实验室录包。
5. **集成式 Web 诊断仪表台**：
   - 模块自带 192.168.4.1 AP 热点，提供车型配置、CAN 总线流量实时监控、总线录包与 OTA 固件更新。

---

## 🛠️ 工程文档与快速索引

| 序号 | 文档名称 | 核心内容 |
| :---: | :--- | :--- |
| **01** | [硬件选型与方案对比指南](file:///D:/DSHbot/t2can-universal-unlock/docs/01_硬件选型与方案对比.md) | ESP32-S3 双 CAN 硬件架构、LILYGO T-2CAN 参数、DIY 方案对比、16V 车载供电与免破线线束选型 |
| **02** | [硬件修改与物理焊接实操指南](file:///D:/DSHbot/t2can-universal-unlock/docs/02_硬件修改与物理焊接实操.md) | **★ 拆除板载两颗 120Ω 终端电阻的理论原理与焊接定位**、RF 外部天线引出、电源抗浪涌防反接改造 |
| **03** | [软件架构与车型适配指南](file:///D:/DSHbot/t2can-universal-unlock/docs/03_软件架构与车型适配指南.md) | 五大车型 Profile 矩阵、Pure Header 代码分层架构、PlatformIO / Arduino IDE 编译烧录与实车调试 |

---

## 🚀 快速开始与编译烧录

### 1. 硬件准备
* **核心板卡**：LILYGO T-2CAN（ESP32-S3，16MB Flash，8MB PSRAM）。
* **硬件修改**：**必须拆除 CAN A 与 CAN B 旁边的 120Ω 贴片终端电阻**（详见 [硬件修改实操指南](file:///D:/DSHbot/t2can-universal-unlock/docs/02_硬件修改与物理焊接实操.md)）。
* **专用线束**：根据车型年份采购特斯拉中控扶手箱后部或网关对插无损线束。

### 2. 软件构建 (PlatformIO)
本工程已配置好完整的 [platformio.ini](file:///D:/DSHbot/t2can-universal-unlock/platformio.ini) 与 [partitions_16mb.csv](file:///D:/DSHbot/t2can-universal-unlock/partitions_16mb.csv)：

```bash
# 进入工程目录
cd D:\DSHbot\t2can-universal-unlock

# 编译固件
pio run

# 烧录固件至 ESP32-S3
pio run --target upload

# 打开串口调试输出
pio run --target monitor
```

### 3. 上电与车型配置
1. 模块接电启动后，手机连接 Wi-Fi：`T2CAN-****`（密码：`12345678`）；
2. 浏览器打开 `http://192.168.4.1`；
3. 进入 **Profile Setup**，选择与实车相符的配置（如 Model 3 Highland 需确认选择加装拨杆还是方向盘按键打灯）；
4. 保存后系统进入正常工作模式，在仪表台上可查看 CAN 数据收发帧率。
