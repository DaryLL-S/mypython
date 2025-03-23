import math
import time
import random


def generate_seal(name="契約", width=40):
    # 配置全角字符确保对齐
    elements = {
        'circle': '◎◆◈◉○◌◍◎◆◈◉',
        'decor': '✦✧✩✪✫✬✭✮✯❂❀✢✣✤✥',
        'text': '臨兵闘者皆陣列在前'
    }

    # 创建画布
    canvas = [['　' for _ in range(width)] for _ in range(width // 2)]

    # 绘制同心圆
    def draw_circle(r, chars):
        for y in range(-r, r + 1):
            for x in range(-r * 2, r * 2 + 1):
                dx = x * 0.5
                if 0.9 < abs(math.sqrt(dx ** 2 + y ** 2) - r < 1.1:
                    canvas[y + center][x + center * 2] = random.choice(chars)


    # 中心坐标
    center = width // 4
    text_len = len(name.encode('gbk'))  # 考虑中文字符宽度

    # 绘制元素
    for r in [12, 10, 8]:
        draw_circle(r, elements['circle'])

    # 添加中心文字
    name_pos = center * 2 - text_len
    for i, char in enumerate(name):
        canvas[center][name_pos + i * 2] = f'\033[31m{char}\033[0m'  # 红色文字

    # 添加装饰符文
    for _ in range(50):
        y = random.randint(2, center * 2 - 2)
        x = random.randint(2, width - 2)
        if canvas[y][x] == '　':
            canvas[y][x] = random.choice(elements['decor'] + elements['text'])

    # 输出结果
    print('\n'.join([''.join(row) for row in canvas]))


if __name__ == "__main__":
    # 生成示例
    generate_seal(name="夏目友人帳")