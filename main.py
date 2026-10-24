# -*- coding: utf-8 -*-
# THOI GIAN BIEU 10/1 - Pygame cho Pydroid 3 (v18 - Mở lên ở trạng thái chờ + Chống tự thoát)
import pygame
import json
import os
import time

os.environ['SDL_ANDROID_TRAP_BACK_BUTTON'] = '1'

pygame.init()
pygame.display.set_caption("Thời Gian Biểu 10/1 - v18")

info = pygame.display.Info()
W, H = max(320, info.current_w), max(480, info.current_h)
screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
clock = pygame.time.Clock()

BG = (18, 24, 38)
PANEL = (30, 41, 59)
PANEL2 = (45, 61, 88)
BORDER = (64, 85, 120)
WHITE = (240, 246, 252)
MUTED = (148, 163, 184)
CYAN = (56, 189, 248)
PINK = (244, 63, 94)
YELLOW = (250, 204, 21)
GREEN = (74, 222, 128)
BLUE = (96, 165, 250)
PURPLE = (192, 132, 252)
ORANGE = (251, 146, 60)
RED = (239, 68, 68)

FONT_PATH = None
possible_fonts = [
    "/system/fonts/Roboto-Regular.ttf",
    "/system/fonts/Roboto-Bold.ttf",
    "/system/fonts/NotoSansCJK-Regular.ttc",
    "/system/fonts/DroidSansFallback.ttf",
    "C:\Windows\Fonts\arial.ttf",
    "C:\Windows\Fonts\segoeui.ttf",
]
for f in possible_fonts:
    if os.path.exists(f):
        FONT_PATH = f
        break

def get_font(size):
    try:
        if FONT_PATH:
            return pygame.font.Font(FONT_PATH, int(size))
        return pygame.font.SysFont("arial", int(size))
    except Exception:
        return pygame.font.Font(None, int(size))

DAYS = [("Thứ 2", 2), ("Thứ 3", 3), ("Thứ 4", 4), ("Thứ 5", 5),
        ("Thứ 6", 6), ("Thứ 7", 7), ("Chủ Nhật", 1)]
DAY_NAMES = {1: "CHỦ NHẬT", 2: "THỨ 2", 3: "THỨ 3", 4: "THỨ 4",
             5: "THỨ 5", 6: "THỨ 6", 7: "THỨ 7"}

FIXED = [
    ("05:45-06:00", "Thức dậy, vệ sinh cá nhân"),
    ("06:00-06:45", "Tập thể dục buổi sáng"),
    ("06:45-07:15", "Chuẩn bị và ăn sáng"),
    ("07:15-08:30", "Đọc bài, xem trước bài học"),
    ("08:45-10:15", "Học thêm cố định"),
    ("10:15-11:15", "Nấu cơm trưa, sơ chế đồ ăn tối"),
    ("11:15-11:30", "Ăn trưa"),
    ("11:30-12:00", "Tắm rửa, vệ sinh cá nhân"),
    ("12:00-12:20", "Rửa bát, dọn dẹp"),
    ("12:20-12:30", "Chuẩn bị balo, thay đồng phục"),
    ("12:30-12:45", "Di chuyển đến trường"),
    ("12:45-17:15", "Học chính khóa lớp 10/1"),
    ("17:15-18:00", "Về phòng, nghỉ ngơi"),
    ("18:00-19:00", "Chuẩn bị và ăn tối"),
    ("19:00-21:30", "Tự học buổi tối"),
    ("21:30-22:30", "Giải trí, thư giãn"),
    ("22:30", "Đi ngủ đúng giờ"),
]

STUDY = {
    2: [("19:00-19:50", "Toán: bài tập đại số / hình học"),
        ("19:55-20:45", "Hóa: hóa trị, phương trình"),
        ("20:50-21:30", "Sinh: đọc bài, trả lời câu hỏi")],
    3: [("19:00-19:45", "Ngữ văn: soạn bài mới"),
        ("19:50-20:35", "Ngoại ngữ: từ vựng, ngữ pháp"),
        ("20:40-21:10", "Hóa học: bài tập"),
        ("21:10-21:30", "Lịch sử: ôn ý chính")],
    4: [("19:00-19:50", "Toán: luyện đề"),
        ("19:55-20:45", "Ngoại ngữ: nghe, đọc hiểu"),
        ("20:50-21:20", "Sinh học: sơ đồ tư duy"),
        ("21:20-21:30", "Xem trước bài GDQP-AN")],
    5: [("19:00-19:50", "Vật lý: bài tập chương mới"),
        ("19:55-20:45", "Tin học: lý thuyết, lập trình"),
        ("20:50-21:30", "HDTN: bài hướng nghiệp")],
    6: [("19:00-20:00", "Ôn tập tuần, sửa lỗi sai"),
        ("20:10-21:30", "Hoàn thành bài tập học thêm")],
    7: [("Buổi sáng", "Học thêm nếu có, dọn dẹp phòng"),
        ("Buổi chiều", "Giặt quần áo, đi chợ"),
        ("Buổi tối", "Nghỉ ngơi, giải trí")],
    1: [("Ban ngày", "Thư giãn, chuẩn bị tuần mới"),
        ("19:00-19:45", "Vật lý: bài tập, công thức"),
        ("19:50-20:35", "Ngữ văn: đọc trước bài"),
        ("20:40-21:10", "Tin học: ôn lý thuyết"),
        ("21:10-21:30", "HDTN: chuẩn bị nội dung")],
}

MEALS = {
    2: ("Trứng đúc thịt băm, canh cải xanh", "Thịt băm rang, rau muống luộc"),
    3: ("Đậu hũ sốt cà chua thịt băm", "Cá nục kho cà chua"),
    4: ("Thịt rang, canh bầu nấu tôm", "Thịt rang hâm nóng, rau cải luộc"),
    5: ("Gà kho gừng sả, canh bắp cải", "Gà kho hâm nóng, canh mồng tơi"),
    6: ("Cá ba sa kho, canh bí đao", "Trứng chiên hành tây, rau lang luộc"),
    7: ("Sườn xào chua ngọt, canh khổ qua", "Món ăn tùy thích"),
    1: ("Tôm rạm, canh rau ngót nấu tôm", "Đậu hũ chiên, canh dưa chua"),
}

TASKS = [
    "Tập thể dục buổi sáng (06:00-06:45)",
    "Tự chuẩn bị bữa trưa (10:15-11:15)",
    "Tắm rửa, vệ sinh cá nhân (11:30)",
    "Hoàn thành tự học buổi tối",
    "Chuẩn bị sách vở cho ngày mai",
]

SAVE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "thoigianbieu_v18_data.json")

day = None
checked = [False] * len(TASKS)
remaining = 45 * 60
timer_running = False  # ĐẶT LẠI: Mở lên ở trạng thái CHỜ (Paused), không tự đếm ngược nữa
last_tick = time.monotonic()
scroll_y = 0
notice = ""
notice_until = 0

day_buttons = []
task_checkboxes = []
reset_task_btn = None
pomo_start_btn = None
pomo_stop_btn = None
pomo_add5_btn = None
pomo_sub5_btn = None
pomo_reset_btn = None

try:
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        saved = json.load(f)
    saved_day = saved.get("day")
    if saved_day in DAY_NAMES:
        day = saved_day
    checked = (saved.get("checked", []) + [False] * len(TASKS))[:len(TASKS)]
    saved_rem = saved.get("remaining")
    if saved_rem is not None and isinstance(saved_rem, (int, float)):
        remaining = max(0, saved_rem)
except Exception:
    pass

def save_data():
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump({"day": day, "checked": checked, "remaining": remaining}, f, ensure_ascii=False)
    except Exception:
        pass

def text(s, x, y, color=WHITE, font=None):
    surf = font.render(str(s), True, color)
    screen.blit(surf, (int(x), int(y)))
    return surf.get_width(), surf.get_height()

def panel(rect, color=PANEL, border=BORDER, radius=16):
    pygame.draw.rect(screen, color, rect, border_radius=radius)
    pygame.draw.rect(screen, border, rect, 2, border_radius=radius)

def button(rect, label, fill, active=False, font=None):
    pygame.draw.rect(screen, fill, rect, border_radius=14)
    if active:
        pygame.draw.rect(screen, WHITE, rect, 4, border_radius=14)
    surf = font.render(label, True, WHITE)
    screen.blit(surf, surf.get_rect(center=rect.center))

def wrap_words(s, max_width, font):
    words = s.split()
    lines, current = [], ""
    for word in words:
        test = (current + " " + word).strip()
        if font.size(test)[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

def draw():
    global W, H, scroll_y, screen
    global day_buttons, task_checkboxes, reset_task_btn, pomo_start_btn, pomo_stop_btn, pomo_add5_btn, pomo_sub5_btn, pomo_reset_btn
    
    display_screen = screen
    W, H = display_screen.get_size()
    
    screen = pygame.Surface((W, max(H, 4200)))
    screen.fill(BG)
    margin = 12
    usable = W - margin * 2

    title_font = get_font(max(40, min(56, int(W * .095))))
    head_font = get_font(max(32, min(44, int(W * .075))))
    small_font = get_font(max(26, min(36, int(W * .060))))
    task_font = get_font(max(30, min(42, int(W * .068))))
    btn_font = get_font(max(24, min(36, int(W * .058))))
    timer_font = get_font(max(85, min(120, int(W * .24))))

    y = 12
    def add_panel(height):
        nonlocal y
        rect = pygame.Rect(margin, y, usable, height)
        panel(rect, PANEL, BORDER, 16)
        y += height + 16
        return rect

    # 1. Tiêu đề
    text("THỜI GIAN BIỂU 10/1", margin+2, y, CYAN, title_font)
    y += title_font.get_linesize() + 4
    text("LỊCH HỌC  •  POMODORO  •  KỶ LUẬT", margin+3, y, MUTED, small_font)
    y += small_font.get_linesize() + 12

    # 2. Pomodoro (5 nút điều khiển)
    r = add_panel(260)
    text("THỜI GIAN HỌC TẬP (POMODORO)", r.x+15, r.y+15, YELLOW, head_font)
    mm, ss = divmod(max(0, int(remaining)), 60)
    surf = timer_font.render(f"{mm:02d}:{ss:02d}", True, CYAN)
    screen.blit(surf, surf.get_rect(center=(W//2, r.y+95)))
    
    gap = 6
    bw = (usable - 30 - gap * 4) // 5
    by = r.y + 165
    pomo_start_btn = pygame.Rect(r.x+15, by, bw, 65)
    pomo_stop_btn = pygame.Rect(r.x+15+(bw+gap), by, bw, 65)
    pomo_add5_btn = pygame.Rect(r.x+15+(bw+gap)*2, by, bw, 65)
    pomo_sub5_btn = pygame.Rect(r.x+15+(bw+gap)*3, by, bw, 65)
    pomo_reset_btn = pygame.Rect(r.x+15+(bw+gap)*4, by, bw, 65)
    
    button(pomo_start_btn, "CHẠY", GREEN, font=btn_font)
    button(pomo_stop_btn, "DỪNG", BLUE, font=btn_font)
    button(pomo_add5_btn, "+5p", ORANGE, font=btn_font)
    button(pomo_sub5_btn, "-5p", RED, font=btn_font)
    button(pomo_reset_btn, "ĐẶT LẠI", PURPLE, font=btn_font)

    # 3. NHIỆM VỤ KỶ LUẬT HẰNG NGÀY
    task_checkboxes = []
    task_item_h = 90  
    task_h = 75 + len(TASKS) * task_item_h + 75
    r = add_panel(task_h)
    text("NHIỆM VỤ KỶ LUẬT HẰNG NGÀY", r.x+15, r.y+15, GREEN, head_font)
    
    for i, task in enumerate(TASKS):
        yy = r.y + 60 + i * task_item_h
        box = pygame.Rect(r.x+15, yy+12, 58, 58)
        click_area = pygame.Rect(r.x+10, yy, usable-20, task_item_h - 6)
        task_checkboxes.append((click_area, i))
        
        pygame.draw.rect(screen, GREEN if checked[i] else BORDER, box, border_radius=12)
        pygame.draw.rect(screen, GREEN if checked[i] else MUTED, box, 4, border_radius=12)
        if checked[i]:
            text("✓", box.x+12, box.y+4, BG, task_font)
            
        lines = wrap_words(task, usable-105, task_font)
        text(lines[0], r.x+90, yy+18, GREEN if checked[i] else WHITE, task_font)
        
    count = sum(checked)
    footer_y = r.y + 60 + len(TASKS) * task_item_h + 10
    text(f"TIẾN ĐỘ: {count}/{len(TASKS)}", r.x+15, footer_y+12, CYAN, head_font)
    reset_task_btn = pygame.Rect(r.right-185, footer_y, 170, 60)
    button(reset_task_btn, "LÀM LẠI", PANEL2, font=head_font)

    # 4. CHỌN THỨ
    day_buttons = []
    btn_h = 85
    panel_days_h = 60 + (btn_h * 3) + 28
    r = add_panel(panel_days_h)
    text("CHỌN THỨ (BẤM ĐỂ HIỆN / BẤM LẠI ĐỂ ẨN)", r.x+15, r.y+15, CYAN, head_font)
    
    w_row1 = (usable - 30 - 2 * 10) // 3
    for i in range(3):
        label, d = DAYS[i]
        bx = r.x + 15 + i * (w_row1 + 10)
        rect = pygame.Rect(bx, r.y + 55, w_row1, btn_h)
        is_active = (day == d)
        button(rect, label, PINK if is_active else PANEL2, is_active, head_font)
        day_buttons.append((rect, d))

    for i in range(3):
        label, d = DAYS[3 + i]
        bx = r.x + 15 + i * (w_row1 + 10)
        rect = pygame.Rect(bx, r.y + 55 + btn_h + 10, w_row1, btn_h)
        is_active = (day == d)
        button(rect, label, PINK if is_active else PANEL2, is_active, head_font)
        day_buttons.append((rect, d))

    label, d = DAYS[6]
    rect = pygame.Rect(r.x + 15, r.y + 55 + (btn_h * 2) + 20, usable - 30, btn_h)
    is_active = (day == d)
    button(rect, label, PINK if is_active else PANEL2, is_active, head_font)
    day_buttons.append((rect, d))

    # 5. Lịch trình chi tiết
    if day is not None:
        schedule_items = []
        if day in range(2, 7):
            schedule_items.append(("KHUNG GIỜ CỐ ĐỊNH (T2-T6)", None, YELLOW, head_font))
            for tm, desc in FIXED:
                schedule_items.append((desc, tm, WHITE, small_font))
        
        schedule_items.append(("KẾ HOẠCH TỰ HỌC RIÊNG", None, CYAN, head_font))
        for tm, desc in STUDY[day]:
            schedule_items.append((desc, tm, WHITE, small_font))
        
        schedule_items.append(("THỰC ĐƠN HÔM NAY", None, GREEN, head_font))
        lunch, dinner = MEALS[day]
        schedule_items.extend([("Trưa: " + lunch, None, WHITE, small_font), 
                               ("Tối: " + dinner, None, WHITE, small_font)])

        inner_width = usable - 32
        time_width = min(170, int(usable * .32))
        schedule_h = 65
        for desc, tm, color, font in schedule_items:
            maxw = inner_width if tm is None else inner_width - time_width - 10
            schedule_h += max(1, len(wrap_words(desc, maxw, font))) * (font.get_linesize() + 6) + (8 if tm is None else 3)

        r_sched = add_panel(schedule_h)
        text("LỊCH TRÌNH - " + DAY_NAMES[day], r_sched.x+15, r_sched.y+15, CYAN, head_font)
        yy = r_sched.y + 60
        for desc, tm, color, font in schedule_items:
            if tm is None:
                yy += 6
                text(desc, r_sched.x+15, yy, color, font)
                yy += font.get_linesize() + 8
            else:
                text(tm, r_sched.x+15, yy, YELLOW, small_font)
                maxw = inner_width - time_width - 10
                lines = wrap_words(desc, maxw, font)
                for j, ln in enumerate(lines):
                    text(ln, r_sched.x+15+time_width, yy+j*(font.get_linesize()+4), color, font)
                yy += max(small_font.get_linesize(), len(lines)*(font.get_linesize()+4)) + 6

    total_height = y + 20
    max_scroll = max(0, total_height - H)
    scroll_y = max(0, min(scroll_y, max_scroll))

    if notice and time.monotonic() < notice_until:
        box = pygame.Rect(10, H-64, W-20, 54)
        pygame.draw.rect(display_screen, PANEL2, box, border_radius=14)
        pygame.draw.rect(display_screen, YELLOW, box, 2, border_radius=14)
        surf = head_font.render(notice, True, YELLOW)
        display_screen.blit(surf, surf.get_rect(center=box.center))

    display_screen.blit(screen, (0, 0), pygame.Rect(0, scroll_y, W, H))
    screen = display_screen
    pygame.display.flip()

def handle_click(pos):
    global day, remaining, timer_running, last_tick, notice, notice_until, scroll_y, checked
    x, sy = pos
    y = sy + scroll_y

    if pomo_start_btn and pomo_start_btn.collidepoint(x, y):
        if not timer_running and remaining > 0:
            timer_running = True
            last_tick = time.monotonic()
            notice = "Đồng hồ đang chạy"
            notice_until = time.monotonic() + 2
        return
    if pomo_stop_btn and pomo_stop_btn.collidepoint(x, y):
        timer_running = False
        notice = "Đã tạm dừng đồng hồ"
        notice_until = time.monotonic() + 2
        return
    if pomo_add5_btn and pomo_add5_btn.clonepoint if hasattr(pomo_add5_btn, 'clonepoint') else pomo_add5_btn.collidepoint(x, y):
        remaining += 5 * 60
        save_data()
        notice = "Đã cộng thêm 5 phút"
        notice_until = time.monotonic() + 2
        return
    if pomo_sub5_btn and pomo_sub5_btn.collidepoint(x, y):
        remaining = max(0, remaining - 5 * 60)
        save_data()
        notice = "Đã bớt đi 5 phút"
        notice_until.monotonic = time.monotonic() + 2 if hasattr(notice_until, 'monotonic') else 0
        notice_until = time.monotonic() + 2
        return
    if pomo_reset_btn and pomo_reset_btn.collidepoint(x, y):
        timer_running = False
        remaining = 45 * 60
        save_data()
        notice = "Đã đặt lại 45 phút"
        notice_until = time.monotonic() + 2
        return

    for rect, idx in task_checkboxes:
        if rect.collidepoint(x, y):
            checked[idx] = not checked[idx]
            save_data()
            return

    if reset_task_btn and reset_task_btn.collidepoint(x, y):
        checked = [False] * len(TASKS)
        save_data()
        notice = "Đã làm mới nhiệm vụ"
        notice_until = time.monotonic() + 2
        return

    for rect, d in day_buttons:
        if rect.collidepoint(x, y):
            if day == d:
                day = None
                notice = "Đã ẩn nội dung lịch trình"
            else:
                day = d
                notice = f"Đã chọn {DAY_NAMES[d]}"
            notice_until = time.monotonic() + 1.5
            scroll_y = 0
            save_data()
            return

running = True
while running:
    now = time.monotonic()
    if timer_running:
        remaining = max(0, remaining - (now - last_tick))
        last_tick = now
        if remaining <= 0:
            remaining = 0
            timer_running = False
            notice = "Đã học xong 45 phút! Hãy nghỉ ngơi."
            notice_until = now + 5
    else:
        last_tick = now  # Cập nhật liên tục để khi bấm CHẠY không bị nhảy thời gian

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pass
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
        elif event.type == pygame.FINGERDOWN:
            handle_click((int(event.x * W), int(event.y * H)))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pass
            elif event.button == 4:
                scroll_y = max(0, scroll_y - 60)
            elif event.button == 5:
                scroll_y += 60
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pass

    draw()
    clock.tick(30)

save_data()
pygame.quit()
