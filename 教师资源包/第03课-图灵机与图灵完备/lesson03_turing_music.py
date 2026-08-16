"""
第3课 图灵机与图灵完备
教师配套资源：
  1) 简化的「音乐图灵机」Python 模拟
  2) 带 D.C. / Fine 反复结构的标准 MusicXML 乐谱
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

from music21 import note, stream, meter
from _score_utils import (
    make_score, make_part, add_repeat_start, add_repeat_end,
    add_da_capo, add_fine
)


def music_turing_machine(tape):
    """模拟一个读取乐谱的图灵机。

    纸带符号说明：
      - 普通字符串如 'C4'：演奏该音符
      - 'R'：反复记号起点
      - 'F'：Fine，停机
    """
    head = 0
    state = {"repeat_count": 0, "mode": "normal"}
    repeat_pos = None
    played = []

    print("\n【音乐图灵机执行 trace】")
    while head < len(tape):
        symbol = tape[head]
        print(f"  状态={state}  头={head}  读到={symbol}")

        if symbol == "R":
            if state["repeat_count"] == 0:
                repeat_pos = head
                state["repeat_count"] = 1
                head += 1
            else:
                head += 1
        elif symbol == "F":
            print("  停机！乐曲结束。")
            break
        else:
            played.append(symbol)
            head += 1

        # 第一遍走到头后跳回反复起点
        if head >= len(tape) and state["repeat_count"] == 1:
            if repeat_pos is not None:
                head = repeat_pos + 1
                state["repeat_count"] = 2

    return played


def main():
    print("=" * 50)
    print("第3课 图灵机与图灵完备")
    print("=" * 50)

    # 1. 图灵机模拟
    tape = ["C4", "D4", "E4", "R", "F4", "G4", "F"]
    played = music_turing_machine(tape)
    print("\n实际演奏序列：", "-".join(played))

    # 2. 用 music21 生成一段带有 D.C. / Fine 反复逻辑的标准乐谱
    #    演奏路径：A 段 -> 反复 -> A 段 -> Fine 结束
    score = make_score(title="第3课 图灵机与 D.C. al Fine")
    part = make_part(name="旋律", instrument_obj=None)

    m1 = stream.Measure(number=1)
    m1.timeSignature = meter.TimeSignature("4/4")
    m1.append(note.Note("C4", quarterLength=1))
    m1.append(note.Note("D4", quarterLength=1))
    m1.append(note.Note("E4", quarterLength=2))

    m2 = stream.Measure(number=2)
    m2.append(note.Note("F4", quarterLength=1))
    m2.append(note.Note("G4", quarterLength=1))
    m2.append(note.Note("A4", quarterLength=1))
    m2.append(note.Note("G4", quarterLength=1))

    # A 段带反复起止
    add_repeat_start(m1)
    add_repeat_end(m2)

    m3 = stream.Measure(number=3)
    m3.append(note.Note("C4", quarterLength=1))
    m3.append(note.Note("E4", quarterLength=1))
    m3.append(note.Note("G4", quarterLength=2))
    add_fine(m3)

    part.append([m1, m2, m3])
    score.append(part)

    score.write("musicxml", fp=os.path.join(OUTPUT_DIR, "lesson03_turing_music.xml"))
    print("\n【乐谱已导出】lesson03_turing_music.xml")


if __name__ == "__main__":
    main()
