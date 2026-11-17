import os
from PIL import Image, ImageDraw, ImageFont

# Canvas size
WIDTH, HEIGHT = 1400, 1050
img = Image.new("RGB", (WIDTH, HEIGHT), "#0D1117")
draw = ImageDraw.Draw(img)

# Fonts
font_title = ImageFont.truetype("msyh.ttc", 28)
font_subtitle = ImageFont.truetype("msyh.ttc", 15)
font_sec = ImageFont.truetype("msyh.ttc", 20)
font_bold = ImageFont.truetype("msyh.ttc", 17)
font_reg = ImageFont.truetype("msyh.ttc", 14)
font_mono = ImageFont.truetype("arial.ttf", 15)
font_small = ImageFont.truetype("msyh.ttc", 13)

# 1. Header
draw.rectangle([(0, 0), (WIDTH, 90)], fill="#161B22")
draw.text((40, 18), "特斯拉 Model 3 / Y 前排副驾 A 柱/网关线束 ➔ LilyGO T-2CAN 物理接线图", fill="#58A6FF", font=font_title)
draw.text((42, 58), "适用场景: 前排 X179 多总线诊断对插线束 | 双路 CAN (Chassis CAN + Party/Body CAN) 硬件接入", fill="#8B949E", font=font_subtitle)

# Helper function for rounded rectangles
def draw_card(xy, fill="#161B22", outline="#30363D", radius=8):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=2)

# 2. Car side block (Tesla Front X179)
draw_card([(50, 115), (510, 780)])
draw.rectangle([(50, 115), (510, 170)], fill="#1F2937")
draw.text((70, 130), "特斯拉原车端：前排副驾 A 柱 / 踢脚板", fill="#38BDF8", font=font_sec)
draw.text((70, 180), "物理接口: X179 多总线诊断插座 (专用 Y 型分流线束)", fill="#94A3B8", font=font_bold)

# Pin list on Tesla side
tesla_pins = [
    {"pin": "Pin 1 (粗红线)", "sig": "12V ~ 16V 常电", "desc": "低压供电输入 (AMD款实测15.5V~16V)", "color": "#EF4444", "y": 235},
    {"pin": "Pin 20/22 (粗黑线)", "sig": "GND (车身地)", "desc": "电源参考地 / 信号地", "color": "#94A3B8", "y": 315},
    {"pin": "Pin 13 (绿/白绞线)", "sig": "Chassis CAN-H", "desc": "底盘高优先级总线 (High) ➔ 控转向/AP", "color": "#10B981", "y": 415},
    {"pin": "Pin 14 (绿色绞线)", "sig": "Chassis CAN-L", "desc": "底盘高优先级总线 (Low)  ➔ 控转向/AP", "color": "#10B981", "y": 485},
    {"pin": "Pin 2 (黄/蓝绞线)", "sig": "Party CAN-H", "desc": "AP私有/车身总线 (High)  ➔ 状态监听", "color": "#F59E0B", "y": 585},
    {"pin": "Pin 3 (黄色绞线)", "sig": "Party CAN-L", "desc": "AP私有/车身总线 (Low)   ➔ 状态监听", "color": "#F59E0B", "y": 655},
]

for item in tesla_pins:
    y = item["y"]
    draw_card([(70, y), (490, y + 55)], fill="#0F172A", outline=item["color"])
    draw.text((85, y + 8), item["pin"], fill=item["color"], font=font_bold)
    draw.text((250, y + 8), item["sig"], fill="#F8FAFC", font=font_bold)
    draw.text((85, y + 32), item["desc"], fill="#64748B", font=font_small)

draw.text((75, 550), "成对紧密双绞 (绞距 2~3cm) ───┐", fill="#10B981", font=font_small)
draw.text((75, 720), "成对紧密双绞 (绞距 2~3cm) ───┘", fill="#F59E0B", font=font_small)

# 3. Middle Protection & Conditioning block
draw_card([(540, 115), (830, 780)])
draw.rectangle([(540, 115), (830, 170)], fill="#1E293B")
draw.text((565, 130), "中间保护与滤波组件", fill="#E2E8F0", font=font_sec)

# Power Protection details
draw_card([(555, 215), (815, 370)], fill="#0B132B", outline="#EF4444")
draw.text((570, 225), "【电源轨保护】", fill="#F87171", font=font_bold)
draw.text((570, 255), "1. 串联 1A 自恢复保险丝", fill="#E2E8F0", font=font_reg)
draw.text((570, 280), "2. 串联 SS34 肖特基二极管", fill="#E2E8F0", font=font_reg)
draw.text((585, 300), "(防反接，正向压降 ~0.3V)", fill="#94A3B8", font=font_small)
draw.text((570, 322), "3. 并联 SMBJ24A TVS 瞬态管", fill="#E2E8F0", font=font_reg)
draw.text((585, 342), "(吸收 16V 锂电尖峰浪涌)", fill="#94A3B8", font=font_small)

# CAN Bus Conditioning details
draw_card([(555, 405), (815, 745)], fill="#0B132B", outline="#38BDF8")
draw.text((570, 415), "【CAN 物理层规范】", fill="#38BDF8", font=font_bold)
draw.text((570, 448), "• 阻抗纪律:", fill="#FACC15", font=font_bold)
draw.text((580, 473), "原车两端已有 120Ω 终端,", fill="#CBD5E1", font=font_reg)
draw.text((580, 498), "T-2CAN 板载两颗 120Ω", fill="#F87171", font=font_bold)
draw.text((580, 523), "必须手工焊下拆除！", fill="#EF4444", font=font_bold)
draw.text((570, 560), "• 压接规范:", fill="#FACC15", font=font_bold)
draw.text((580, 585), "剥线长 7mm, 必须压接", fill="#CBD5E1", font=font_reg)
draw.text((580, 610), "VE0508 管型冷压端头,", fill="#38BDF8", font=font_reg)
draw.text((580, 635), "严禁散乱多股铜丝直拧!", fill="#F87171", font=font_small)
draw.text((570, 672), "• 走线要求:", fill="#FACC15", font=font_bold)
draw.text((580, 697), "引线长 ≤ 30cm, 阻燃胶布固定", fill="#CBD5E1", font=font_small)

# 4. Board side block (LilyGO T-2CAN)
draw_card([(860, 115), (1350, 780)])
draw.rectangle([(860, 115), (1350, 170)], fill="#1F2937")
draw.text((885, 130), "LilyGO T-2CAN 螺丝接线端子排", fill="#34D399", font=font_sec)
draw.text((885, 180), "ESP32-S3 双通道车载 CAN 开发板端子定义", fill="#94A3B8", font=font_bold)

board_terminals = [
    {"term": "12-24V", "dest": "供电正极输入 (板载宽压 DC-DC)", "color": "#EF4444", "y": 235},
    {"term": "GND", "dest": "供电负极 / 电源参考地", "color": "#94A3B8", "y": 315},
    {"term": "CANHB", "dest": "CAN B High (ESP32-S3 TWAI 原生)", "color": "#10B981", "y": 415},
    {"term": "CANLB", "dest": "CAN B Low  (ESP32-S3 TWAI 原生)", "color": "#10B981", "y": 485},
    {"term": "CANHA", "dest": "CAN A High (MCP2515 外部 SPI)", "color": "#F59E0B", "y": 585},
    {"term": "CANLA", "dest": "CAN A Low  (MCP2515 外部 SPI)", "color": "#F59E0B", "y": 655},
]

for item in board_terminals:
    y = item["y"]
    draw_card([(880, y), (1330, y + 55)], fill="#0F172A", outline=item["color"])
    draw.text((900, y + 8), item["term"], fill=item["color"], font=font_bold)
    draw.text((1000, y + 8), item["dest"], fill="#F8FAFC", font=font_bold)
    draw.text((900, y + 32), "对应固件逻辑通道", fill="#64748B", font=font_small)

draw.text((885, 735), "※ 端子排 SGNDA / DGNDA / SGNDB / DGNDB 保持留空悬空", fill="#64748B", font=font_small)

# 5. Connection Lines (Arrows)
def draw_arrow(p1, p2, color, width=3):
    draw.line([p1, p2], fill=color, width=width)
    x2, y2 = p2
    draw.polygon([(x2, y2), (x2 - 8, y2 - 5), (x2 - 8, y2 + 5)], fill=color)

# Power line
draw_arrow((490, 262), (555, 262), "#EF4444")
draw_arrow((815, 262), (880, 262), "#EF4444")

# GND line
draw_arrow((490, 342), (555, 342), "#94A3B8")
draw_arrow((815, 342), (880, 342), "#94A3B8")

# Chassis CAN H line
draw_arrow((490, 442), (880, 442), "#10B981")
# Chassis CAN L line
draw_arrow((490, 512), (880, 512), "#10B981")

# Party CAN H line
draw_arrow((490, 612), (880, 612), "#F59E0B")
# Party CAN L line
draw_arrow((490, 682), (880, 682), "#F59E0B")

# 6. Bottom Safety & Verification Checklist
draw_card([(50, 805), (1350, 1015)], fill="#161B22", outline="#30363D")
draw.rectangle([(50, 805), (1350, 840)], fill="#1F2937")
draw.text((70, 815), "施工核验纪律（必须严格执行三步法，杜绝烧板与报故障码）", fill="#FACC15", font=font_bold)

steps = [
    ("第 1 步：全车下电静置", "车机选择【控制 ➔ 安全 ➔ 关闭电源】，人留在车内静坐 15 分钟，听到主接触器断开声（咔嗒响），仪表屏幕全黑后方可拔插 A 柱 X179 插头。"),
    ("第 2 步：万用表电压核验", "插上 Y 型线束但暂不接 T-2CAN！用万用表测红黑线：确认电压为 15.5V~16.0V（Ryzen）且极性正确；测 CAN-H 与 CAN-L 对地共模电压应在 2.2V~2.7V 正常区间。"),
    ("第 3 步：冷态上板与冷压端子", "端子线头必须压接 VE0508 管型冷压端头，螺丝锁紧确认无松脱无毛刺；主板焊接确认 R_A 与 R_B 终端电阻已完全脱落阻断，方可开机通电。")
]

for idx, (title, desc) in enumerate(steps):
    y = 855 + idx * 48
    draw.text((70, y), title, fill="#38BDF8", font=font_bold)
    draw.text((270, y), desc, fill="#CBD5E1", font=font_reg)

# Save image
out_path = r"D:\DSHbot\t2can-universal-unlock\docs\images\T2CAN_Front_Wiring_Diagram.png"
os.makedirs(os.path.dirname(out_path), exist_ok=True)
img.save(out_path, "PNG")
print(f"Successfully generated: {out_path}")
