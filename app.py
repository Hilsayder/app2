import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math
import io

st.set_page_config(
    page_title="Визуализатор рекурсивных фракталов", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Визуализатор рекурсивных геометрических фракталов")
st.markdown("Интерактивный программный комплекс к курсовому проекту (П. И. Лукинских, КубГУ).")

# Боковая панель управления
st.sidebar.header("Параметры визуализации")

fractal_choice = st.sidebar.selectbox(
    "Выберите тип фрактала:",
    [
        "Дерево Пифагора",
        "Треугольник Серпинского",
        "Кривая Коха",
        "Дракон Хартера–Хейтуэя",
        "Ковёр Серпинского"
    ]
)

color_theme = st.sidebar.selectbox(
    "Цветовая схема:",
    ["Классическая", "Градиент глубины", "Монохромная (темная)"]
)

# 1. Дерево Пифагора
if fractal_choice == "Дерево Пифагора":
    st.sidebar.subheader("Настройки дерева")
    depth = st.sidebar.slider("Глубина рекурсии (уровни)", 1, 8, 7)
    angle_offset = st.sidebar.slider("Угол ветвления (градусы)", 15, 60, 28)
    shrink = st.sidebar.slider("Коэффициент сжатия ветви", 0.60, 0.82, 0.74, step=0.02)
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    def draw_tree(x, y, angle, length, d):
        if d == 0:
            return
        x2 = x + length * math.cos(math.radians(angle))
        y2 = y + length * math.sin(math.radians(angle))
        
        c = 'forestgreen' if color_theme == "Классическая" else ('darkgreen' if color_theme == "Монохромная (темная)" else plt.cm.viridis(d / depth))
        ax.plot([x, x2], [y, y2], color=c, lw=max(1.0, d * 0.8))
        
        draw_tree(x2, y2, angle + angle_offset, length * shrink, d - 1)
        draw_tree(x2, y2, angle - angle_offset, length * shrink, d - 1)

    draw_tree(0, 0, 90, 100, depth)
    ax.set_aspect('equal')
    ax.axis('off')
    st.pyplot(fig)

# 2. Треугольник Серпинского
elif fractal_choice == "Треугольник Серпинского":
    st.sidebar.subheader("Настройки треугольника")
    depth = st.sidebar.slider("Глубина рекурсии", 0, 7, 5)
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    def draw_sierpinski(p1, p2, p3, d):
        if d == 0:
            col = 'purple' if color_theme == "Классическая" else ('navy' if color_theme == "Монохромная (темная)" else plt.cm.plasma(0.7))
            ax.fill([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], color=col)
        else:
            p12 = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
            p23 = ((p2[0] + p3[0]) / 2, (p2[1] + p3[1]) / 2)
            p31 = ((p3[0] + p1[0]) / 2, (p3[1] + p1[1]) / 2)
            draw_sierpinski(p1, p12, p31, d - 1)
            draw_sierpinski(p12, p2, p23, d - 1)
            draw_sierpinski(p31, p23, p3, d - 1)

    draw_sierpinski((0, 0), (1, 0), (0.5, math.sqrt(3)/2), depth)
    ax.set_aspect('equal')
    ax.axis('off')
    st.pyplot(fig)

# 3. Кривая Коха
elif fractal_choice == "Кривая Коха":
    st.sidebar.subheader("Настройки кривой Коха")
    depth = st.sidebar.slider("Глубина рекурсии", 0, 5, 4)
    
    def koch_curve(p1, p2, d):
        if d == 0:
            return [p1, p2]
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        p3 = (p1[0] + dx / 3, p1[1] + dy / 3)
        p5 = (p1[0] + 2 * dx / 3, p1[1] + 2 * dy / 3)
        px = p1[0] + dx / 2 - dy * math.sqrt(3) / 6
        py = p1[1] + dy / 2 + dx * math.sqrt(3) / 6
        p4 = (px, py)
        return (koch_curve(p1, p3, d - 1)[:-1] + 
                koch_curve(p3, p4, d - 1)[:-1] + 
                koch_curve(p4, p5, d - 1)[:-1] + 
                koch_curve(p5, p2, d - 1))

    p1, p2, p3 = (0, 0), (1, 0), (0.5, math.sqrt(3)/2)
    pts = (koch_curve(p1, p2, depth)[:-1] + 
           koch_curve(p2, p3, depth)[:-1] + 
           koch_curve(p3, p1, depth))
    kx, ky = zip(*pts)

    fig, ax = plt.subplots(figsize=(8, 8))
    line_col = 'royalblue' if color_theme != "Монохромная (темная)" else 'black'
    fill_col = 'aliceblue' if color_theme != "Монохромная (темная)" else 'lightgray'
    ax.plot(kx, ky, color=line_col, lw=1.5)
    ax.fill(kx, ky, color=fill_col, alpha=0.6)
    ax.set_aspect('equal')
    ax.axis('off')
    st.pyplot(fig)

# 4. Дракон Хартера–Хейтуэя
elif fractal_choice == "Дракон Хартера–Хейтуэя":
    st.sidebar.subheader("Настройки дракона")
    order = st.sidebar.slider("Порядок итерации", 1, 14, 11)
    
    def dragon_curve(n):
        turns = []
        for _ in range(n):
            turns = turns + [1] + [-t for t in reversed(turns)]
        x, y, dx, dy = 0, 0, 1, 0
        pts = [(x, y)]
        for turn in turns:
            x, y = x + dx, y + dy
            pts.append((x, y))
            dx, dy = (-dy, dx) if turn == 1 else (dy, -dx)
        pts.append((x + dx, y + dy))
        return pts

    pts = dragon_curve(order)
    dx_vals, dy_vals = zip(*pts)

    fig, ax = plt.subplots(figsize=(8, 8))
    c = 'firebrick' if color_theme == "Классическая" else ('darkmagenta' if color_theme == "Градиент глубины" else 'black')
    ax.plot(dx_vals, dy_vals, color=c, lw=1)
    ax.set_aspect('equal')
    ax.axis('off')
    st.pyplot(fig)

# 5. Ковёр Серпинского
elif fractal_choice == "Ковёр Серпинского":
    st.sidebar.subheader("Настройки ковра")
    depth = st.sidebar.slider("Глубина рекурсии", 0, 5, 4)
    
    fig, ax = plt.subplots(figsize=(8, 8))
    base_color = 'darkslategray' if color_theme != "Монохромная (темная)" else 'black'
    ax.fill([0, 1, 1, 0], [0, 0, 1, 1], color=base_color)

    def draw_carpet(x, y, size, d):
        if d == 0:
            return
        sub = size / 3
        ax.fill([x + sub, x + 2*sub, x + 2*sub, x + sub],
                [y + sub, y + sub, y + 2*sub, y + 2*sub], color='white')
        for i in range(3):
            for j in range(3):
                if not (i == 1 and j == 1):
                    draw_carpet(x + i*sub, y + j*sub, sub, d - 1)

    draw_carpet(0, 0, 1, depth)
    ax.set_aspect('equal')
    ax.axis('off')
    st.pyplot(fig)

# Модуль сохранения изображения в PNG
buf = io.BytesIO()
fig.savefig(buf, format="png", bbox_inches='tight', dpi=200)
st.sidebar.download_button(
    label="Сохранить изображение (PNG)",
    data=buf.getvalue(),
    file_name=f"{fractal_choice}.png",
    mime="image/png"
)
