"""
第11课 卡农的递归结构（本科进阶）
教师配套资源：用递归函数生成多声部卡农
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

from music21 import note, stream, key, meter
from _score_utils import make_score, make_part, renumber_measures


def make_theme(number=1):
    """卡农主题：4 小节，适合循环追逐。"""
    m = stream.Measure(number=number)
    m.timeSignature = meter.TimeSignature("4/4")
    notes_data = [
        ("D4", 1), ("A4", 1), ("F#4", 1), ("A4", 1),
        ("G4", 1), ("A4", 1), ("F#4", 1), ("D4", 1),
        ("E4", 1), ("F#4", 1), ("G4", 1), ("E4", 1),
        ("D4", 2), ("D4", 2),
    ]
    for p, ql in notes_data:
        m.append(note.Note(p, quarterLength=ql))
    return m


def make_canon(voice_num, delay, total_voices=3):
    """递归生成卡农 Score。

    每递归一层添加一个延迟进入的声部。
    """
    print(f"  递归层 voice_num={voice_num}, delay={delay}")
    score = stream.Score()

    # 基线条件：所有声部已添加完毕
    if voice_num > total_voices:
        return score

    # 创建当前声部的主题（延迟进入，主题自身小节编号从 1 开始）
    part = make_part(name=f"声部 {voice_num}")
    theme = make_theme(number=1)
    theme.insert(0, key.Key("D"))   # 调号写入第一小节，避免 Part 级插入产生 measure 0
    part.insert(delay, theme)
    renumber_measures(part)
    score.insert(0, part)

    # 递归步骤：添加下一个声部
    sub_score = make_canon(voice_num + 1, delay + 4, total_voices)
    for p in sub_score.parts:
        score.insert(0, p)

    return score


def main():
    print("第11课 卡农的递归结构")
    print("\n【递归调用 trace】")

    canon = make_canon(voice_num=1, delay=0, total_voices=3)
    score = make_score(title="第11课 三部卡农")
    for p in canon.parts:
        score.append(p)
    score.write("musicxml", fp=os.path.join(OUTPUT_DIR, "lesson11_canon_recursion.xml"))
    print("\n已导出：lesson11_canon_recursion.xml （三部卡农）")


if __name__ == "__main__":
    main()
