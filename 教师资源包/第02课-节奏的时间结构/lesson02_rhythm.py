"""
第2课 节奏的时间结构
教师配套资源：时值、拍号与 Stream 层次体系
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

from music21 import note, stream, meter
from _score_utils import make_score


def make_measure(number, time_sig, notes_data):
    """通用小节工厂函数。

    Args:
        number: 小节编号
        time_sig: 拍号字符串，如 '4/4'
        notes_data: [(音名字符串, 时值), ...]，时值为四分音符的倍数
    """
    m = stream.Measure(number=number)
    m.timeSignature = meter.TimeSignature(time_sig)
    total = 0.0
    for pitch, ql in notes_data:
        if pitch is None:
            n = note.Rest(quarterLength=ql)
        else:
            n = note.Note(pitch, quarterLength=ql)
        m.append(n)
        total += ql
    # 简单校验：小节总时值应等于拍号的 quarterLength
    expected = meter.TimeSignature(time_sig).barDuration.quarterLength
    if abs(total - expected) > 1e-6:
        print(f"  [警告] 第 {number} 小节总时值 {total} 不等于拍号 {time_sig} 的预期 {expected}")
    return m


def main():
    print("第2课 节奏的时间结构")

    # 1. 4/4 拍 4 小节，每小节不同节奏型
    part_4_4 = stream.Part()
    part_4_4.partName = "4/4 拍节奏型"
    data_4_4 = [
        [("C4", 1), ("D4", 1), ("E4", 1), ("F4", 1)],
        [("G4", 2), ("G4", 0.5), ("A4", 0.5), ("G4", 1)],
        [("F4", 0.5), ("F4", 0.5), ("F4", 0.5), ("F4", 0.5), ("E4", 2)],
        [("C4", 1), ("E4", 1), ("G4", 2)],
    ]
    for i, data in enumerate(data_4_4, start=1):
        part_4_4.append(make_measure(i, "4/4", data))

    score_4_4 = make_score(title="第2课 4/4 拍节奏型")
    score_4_4.append(part_4_4)
    score_4_4.write("musicxml", fp=os.path.join(OUTPUT_DIR, "lesson02_rhythm_4_4.xml"))
    print("已导出：lesson02_rhythm_4_4.xml")

    # 2. 3/4 拍同一旋律片段
    part_3_4 = stream.Part()
    part_3_4.partName = "3/4 拍旋律"
    data_3_4 = [
        [("C4", 1), ("E4", 1), ("G4", 1)],
        [("G4", 1), ("A4", 1), ("G4", 1)],
        [("F4", 0.5), ("F4", 0.5), ("E4", 1), ("E4", 1)],
        [("C4", 1), ("E4", 1), ("G4", 1)],
    ]
    for i, data in enumerate(data_3_4, start=1):
        part_3_4.append(make_measure(i, "3/4", data))

    score_3_4 = make_score(title="第2课 3/4 拍旋律")
    score_3_4.append(part_3_4)
    score_3_4.write("musicxml", fp=os.path.join(OUTPUT_DIR, "lesson02_rhythm_3_4.xml"))
    print("已导出：lesson02_rhythm_3_4.xml")

    # 3. 6/8 拍挑战：以八分音符为一拍，每小节 6 拍
    part_6_8 = stream.Part()
    part_6_8.partName = "6/8 拍挑战"
    # quarterLength=0.5 对应一个八分音符
    data_6_8 = [
        [("C4", 0.5), ("D4", 0.5), ("E4", 0.5), ("F4", 0.5), ("G4", 0.5), ("G4", 0.5)],
        [("A4", 1.5), ("G4", 0.5), ("F4", 0.5), ("E4", 0.5)],
        [("D4", 0.5), ("E4", 0.5), ("F4", 0.5), ("D4", 0.5), ("C4", 1)],
    ]
    for i, data in enumerate(data_6_8, start=1):
        part_6_8.append(make_measure(i, "6/8", data))

    score_6_8 = make_score(title="第2课 6/8 拍挑战")
    score_6_8.append(part_6_8)
    score_6_8.write("musicxml", fp=os.path.join(OUTPUT_DIR, "lesson02_rhythm_6_8.xml"))
    print("已导出：lesson02_rhythm_6_8.xml")

    # 4. 列表推导式批量生成八分音符音阶
    scale_pitches = ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"]
    eighth_measure = stream.Measure(number=1)
    eighth_measure.timeSignature = meter.TimeSignature("4/4")
    eighth_notes = [note.Note(p, quarterLength=0.5) for p in scale_pitches]
    for n in eighth_notes:
        eighth_measure.append(n)

    scale_part = stream.Part()
    scale_part.partName = "八分音符音阶"
    scale_part.append(eighth_measure)

    score_scale = make_score(title="第2课 八分音符音阶")
    score_scale.append(scale_part)
    score_scale.write("musicxml", fp=os.path.join(OUTPUT_DIR, "lesson02_eighth_scale.xml"))
    print("已导出：lesson02_eighth_scale.xml")


if __name__ == "__main__":
    main()
