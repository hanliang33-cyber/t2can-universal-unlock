import os
import math
from PIL import Image, ImageDraw, ImageFont

# Set up canvas
width = 1400
height = 920
img = Image.new("RGB", (width, height), "#0f172a") # Slate 900 background
draw = ImageDraw.Draw(img)

# Fonts
font_dir = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts')
font_path_cn = os.path.join(font_dir, 'msyh.ttc')
font_path_bold = os.path.join(font_dir, 'msyhbd.ttc')
if not os.path.exists(font_path_bold):
    font_path_bold = font_path_cn

title_font = ImageFont.truetype(font_path_bold, 28)
sub_font = ImageFont.truetype(font_path_cn, 16)
sec_font = ImageFont.truetype(font_path_bold, 18)
body_font = ImageFont.truetype(font_path_cn, 14)
bold_font = ImageFont.truetype(font_path_bold, 14)
small_font = ImageFont.truetype(font_path_cn, 12)
pin_font = ImageFont.truetype(font_path_bold, 12)

# 1. Header
draw.rectangle([(0, 0), (width, 80)], fill="#1e293b")
draw.line([(0, 80), (width, 80)], fill="#334155", width=2)
draw.text((40, 18), "LilyGO T-2CAN 车载接入接线指示图 (Tesla Model 3 / Y)", font=title_font, fill="#f8fafc")
draw.text((40, 52), "适用车型: 2022~2023 Model Y (AMD Ryzen 16V低压) | 诊断口: 后排出风口 26-Pin 蓝色母头", font=sub_font, fill="#94a3b8")

# Helper function for rounded rectangles
def draw_rounded_rect(draw_obj, box, radius, fill, outline=None, width=1):
    x1, y1, x2, y2 = box
    draw_obj.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=width)

# Helper function for drawing wavy twisted pair lines
def draw_twisted_pair(draw_obj, p1, p2, color1, color2, label, label_color="#38bdf8"):
    # p1 = (x1, y1), p2 = (x2, y2)
    # Draw two sine waves between p1 and p2 along the y-axis
    x1, y1 = p1
    x2, y2 = p2
    steps = 150
    points1 = []
    points2 = []
    dy = y2 - y1
    dx = x2 - x1
    for i in range(steps + 1):
        t = i / steps
        cur_y = y1 + dy * t
        cur_base_x = x1 + dx * t
        # sine offset
        offset = 8 * math.sin(t * math.pi * 12) # 6 twists
        points1.append((cur_base_x + offset, cur_y))
        points2.append((cur_base_x - offset, cur_y))
    
    # Draw lines
    for i in range(len(points1) - 1):
        draw_obj.line([points1[i], points1[i+1]], fill=color1, width=3)
        draw_obj.line([points2[i], points2[i+1]], fill=color2, width=3)
    
    # Draw label box in middle
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    box_w = 150
    box_h = 24
    draw_rounded_rect(draw_obj, (mid_x - box_w/2, mid_y - box_h/2, mid_x + box_w/2, mid_y + box_h/2), 6, "#1e293b", "#475569", 1)
    draw_obj.text((mid_x - box_w/2 + 8, mid_y - 8), label, font=small_font, fill=label_color)

# 2. Left Box: Tesla 26-Pin Connector
draw_rounded_rect(draw, (40, 110, 420, 520), 12, "#1e293b", "#3b82f6", 2)
# Badge
draw_rounded_rect(draw, (55, 125, 260, 155), 6, "#1d4ed8")
draw.text((65, 130), "原车 26-Pin 诊断插头引脚", font=sec_font, fill="#ffffff")

draw.text((55, 170), "插头规格: TE / 汽车微型 26-Pin 胶壳", font=body_font, fill="#cbd5e1")
draw.text((55, 195), "引出线共计 6 根（电源 2 根 + CAN 4 根）：", font=body_font, fill="#94a3b8")

# Pins list in Tesla connector
pins_data = [
    ("Pin 1", "15.5V~16V 常电 (+)", "#ef4444", 230),
    ("Pin 20", "GND 整车地 (-)", "#64748b", 280),
    ("Pin 2", "Body CAN-High (500k)", "#3b82f6", 340),
    ("Pin 3", "Body CAN-Low (500k)", "#0284c7", 390),
    ("Pin 13", "Chassis CAN-High (500k)", "#f97316", 445),
    ("Pin 14", "Chassis CAN-Low (500k)", "#eab308", 485),
]

for pin, desc, col, y_pos in pins_data:
    draw_rounded_rect(draw, (55, y_pos - 4, 130, y_pos + 26), 6, "#0f172a", col, 2)
    draw.text((68, y_pos + 2), pin, font=bold_font, fill="#f8fafc")
    draw.text((140, y_pos + 2), desc, font=body_font, fill=col)

# 3. Right Box: LilyGO T-2CAN Board
draw_rounded_rect(draw, (850, 110, 1360, 520), 12, "#1e293b", "#10b981", 2)
draw_rounded_rect(draw, (865, 125, 1080, 155), 6, "#047857")
draw.text((875, 130), "LilyGO T-2CAN 开发板端子", font=sec_font, fill="#ffffff")

draw.text((865, 170), "主控: ESP32-S3 | 双路 CAN (MCP2515 + TWAI)", font=body_font, fill="#cbd5e1")
draw.text((865, 195), "请对照板载螺丝端子丝印接线：", font=body_font, fill="#94a3b8")

# Right terminals
terminals_data = [
    ("12-24V", "DC 宽压输入正极", "#ef4444", 230),
    ("GND", "系统供电总地", "#64748b", 280),
    ("CANHA", "CAN A 高电平 (MCP2515)", "#3b82f6", 340),
    ("CANLA", "CAN A 低电平 (MCP2515)", "#0284c7", 390),
    ("CANHB", "CAN B 高电平 (ESP32-TWAI)", "#f97316", 445),
    ("CANLB", "CAN B 低电平 (ESP32-TWAI)", "#eab308", 485),
]

for term, desc, col, y_pos in terminals_data:
    draw_rounded_rect(draw, (865, y_pos - 4, 955, y_pos + 26), 6, "#0f172a", col, 2)
    draw.text((875, y_pos + 2), term, font=bold_font, fill="#f8fafc")
    draw.text((968, y_pos + 2), desc, font=body_font, fill=col)

# 4. Middle Wiring Connections & Components
# Line 1: Pin 1 (16V) -> Protection -> 12-24V
p1_start = (420, 243)
p1_end = (865, 243)
# Draw protective components along line 1
draw.line([(420, 243), (480, 243)], fill="#ef4444", width=3)
# Fuse component
draw_rounded_rect(draw, (480, 230, 570, 256), 4, "#334155", "#ef4444", 1)
draw.text((488, 235), "1A 自恢复保险", font=small_font, fill="#fca5a5")
draw.line([(570, 243), (610, 243)], fill="#ef4444", width=3)
# Diode component
draw_rounded_rect(draw, (610, 230, 710, 256), 4, "#334155", "#ef4444", 1)
draw.text((618, 235), "SS34 防反二极管", font=small_font, fill="#fca5a5")
draw.line([(710, 243), (865, 243)], fill="#ef4444", width=3)

# Line 2: Pin 20 (GND) -> GND
draw.line([(420, 293), (865, 293)], fill="#64748b", width=3)
# TVS Diode between 16V and GND at x=780
draw.line([(780, 243), (780, 260)], fill="#ef4444", width=2)
draw_rounded_rect(draw, (735, 260, 825, 282), 4, "#1e293b", "#f59e0b", 1)
draw.text((742, 264), "SMBJ24A TVS", font=small_font, fill="#fde047")
draw.line([(780, 282), (780, 293)], fill="#64748b", width=2)
draw.text((640, 300), "20AWG (0.5mm²) 红/黑车规耐温线", font=small_font, fill="#94a3b8")

# CAN Pairs: Twisted
draw_twisted_pair(draw, (420, 365), (865, 365), "#3b82f6", "#38bdf8", "Body CAN 独立双绞", "#38bdf8")
draw_twisted_pair(draw, (420, 465), (865, 465), "#f97316", "#facc15", "Chassis CAN 独立双绞", "#fbbf24")

# 5. Bottom Instructions & Notes (Cards)
card_y = 550
card_h = 330
card_w = (width - 80 - 40) / 3 # 3 cards

# Card 1: 制作工艺要点
draw_rounded_rect(draw, (40, card_y, 40 + card_w, card_y + card_h), 10, "#1e293b", "#334155", 1)
draw_rounded_rect(draw, (55, card_y + 15, 55 + 130, card_y + 42), 4, "#3b82f6")
draw.text((65, card_y + 19), "1. 自制线束工艺", font=bold_font, fill="#ffffff")

c1_lines = [
    "• 双绞节距: 每米 30~50 节 (2~3cm 一扭)。",
    "• 解绞长度: 尾端接入端子暴露部分 ≤ 20mm。",
    "• 严禁混绞: Body CAN 与 Chassis CAN 各自",
    "  成对独立双绞，绝对不能 4 根绞在一起。",
    "• 电源隔离: 16V/GND 电源线不得与 CAN 线",
    "  绑入同一绞线股，防止脉冲噪声耦合。",
    "• 端头压接: 线头务必压接 VE 管型冷压端头",
    "  (针形)，严禁散铜丝直接拧入螺丝端子。"
]
for idx, line in enumerate(c1_lines):
    draw.text((55, card_y + 55 + idx * 32), line, font=small_font, fill="#cbd5e1")

# Card 2: 关键硬件修改 (强制)
draw_rounded_rect(draw, (40 + card_w + 20, card_y, 40 + 2*card_w + 20, card_y + card_h), 10, "#1e293b", "#ef4444", 2)
draw_rounded_rect(draw, (55 + card_w + 20, card_y + 15, 55 + card_w + 20 + 150, card_y + 42), 4, "#dc2626")
draw.text((65 + card_w + 20, card_y + 19), "2. 强制硬件修改 (必做)", font=bold_font, fill="#ffffff")

c2_lines = [
    "★ 焊下板载两颗 120Ω 贴片终端电阻！",
    "  - 原因: 原车两端已自带终端电阻 (等效 60Ω)。",
    "  - 若不拆除: T-2CAN 接入后整车阻抗暴跌至",
    "    30~40Ω，差分电压失真，网关立刻报故障",
    "    码并直接禁用辅助驾驶 (AP)。",
    "  - 位置: CANHA/LA 侧贴片电阻 R_A (120Ω)",
    "         CANHB/LB 侧贴片电阻 R_B (120Ω)",
    "  - 验收: 拆后万用表量板端 H/L 间应开路/无穷大。"
]
for idx, line in enumerate(c2_lines):
    fill_c = "#fca5a5" if "★" in line or "若不拆除" in line else "#cbd5e1"
    draw.text((55 + card_w + 20, card_y + 55 + idx * 32), line, font=small_font, fill=fill_c)

# Card 3: 上车验证与防呆
draw_rounded_rect(draw, (40 + 2*card_w + 40, card_y, 40 + 3*card_w + 40, card_y + card_h), 10, "#1e293b", "#334155", 1)
draw_rounded_rect(draw, (55 + 2*card_w + 40, card_y + 15, 55 + 2*card_w + 40 + 130, card_y + 42), 4, "#10b981")
draw.text((65 + 2*card_w + 40, card_y + 19), "3. 上车打表防呆", font=bold_font, fill="#ffffff")

c3_lines = [
    "• 测电压: 26P 转接线插上原车后，先不插板子，",
    "  用万用表测引出的红黑线电压:",
    "  - 红笔接红、黑笔接黑: 实测约 +15.5V~16V。",
    "• 测总线: 测量 CAN_H 与 CAN_L 间电压:",
    "  - 正常在 2.3V ~ 2.7V 之间动态微幅波动。",
    "• 悬空端子: 板端的 SGNDA/DGNDA/SGNDB 属于",
    "  隔离地/屏蔽地，出风口短线场景直接【悬空】。",
    "• 包覆防异响: 验收后全线束用德莎绒布胶带缠绕。"
]
for idx, line in enumerate(c3_lines):
    draw.text((55 + 2*card_w + 40, card_y + 55 + idx * 32), line, font=small_font, fill="#cbd5e1")

# Save image
output_path = "D:\\DSHbot\\t2can-universal-unlock\\docs\\images\\T2CAN_Wiring_Diagram.png"
img.save(output_path, "PNG")
print("Saved to", output_path)
