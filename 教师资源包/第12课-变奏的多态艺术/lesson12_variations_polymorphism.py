"""
第12课 变奏的多态艺术（本科进阶）
教师配套资源：高阶函数/多态处理同一主题
生成主题 + 装饰加花 + 节奏加密 + 小调变奏
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

import copy
from music21 import note, stream, key, meter
from _score_utils import make_score, make_part, add_double_barline, renumber_measures


def make_theme(number=1):
    """小星星主题（4 小节）。"""
    pitches = ["C4", "C4", "G4", "G4", "A4", "A4", "G4",
               "F4", "F4", "E4", "E4", "D4", "D4", "C4"]
    durations = [1] * 14
    notes_list = []
    for p, d in zip(pitches, durations):
        notes_list.append(note.Note(p, quarterLength=d))

    # 把 14 个四分音符拆成 4 小节（4+4+4+2）
    measures = []
    beats_per_measure = 4.0
    current = stream.Measure(number=number)
    current.timeSignature = meter.TimeSignature("4/4")
    current_len = 0.0
    measure_num = number

    for n in notes_list:
        ql = n.quarterLength
        if current_len + ql > beats_per_measure + 1e-9 and current_len > 0:
            measures.append(current)
            measure_num += 1
            current = stream.Measure(number=measure_num)
            current.timeSignature = meter.TimeSignature("4/4")
            current_len = 0.0
        current.append(n)
        current_len += ql
    measures.append(current)

    # 返回一个包含 4 个小节的 Part
    part = stream.Part()
    for m in measures:
        part.append(m)
    return part


def var_ornament(theme_part):
    """装饰加花：在长音前插入上方邻音。"""
    result = stream.Part()
    for theme_measure in theme_part.getElementsByClass(stream.Measure):
        m = stream.Measure(number=theme_measure.number)
        for n in theme_measure.notes:
            if n.quarterLength >= 1:
                neighbor = n.transpose(1)
                m.append(note.Note(neighbor.pitch.nameWithOctave, quarterLength=0.25))
                m.append(note.Note(n.pitch.nameWithOctave, quarterLength=n.quarterLength - 0.25))
            else:
                m.append(note.Note(n.pitch.nameWithOctave, quarterLength=n.quarterLength))
        result.append(m)
    return result


def var_rhythm(theme_part):
    """节奏加密：所有音符时值减半。"""
    result = stream.Part()
    for theme_measure in theme_part.getElementsByClass(stream.Measure):
        m = stream.Measure(number=theme_measure.number)
        for n in theme_measure.notes:
            m.append(note.Note(n.pitch.nameWithOctave, quarterLength=n.quarterLength / 2))
        result.append(m)
    return result


def var_minor(theme_part):
    """转小调：将 E、A、B 降半音（C 大调 -> c 小调效果）。"""
    result = stream.Part()
    for theme_measure in theme_part.getElementsByClass(stream.Measure):
        m = stream.Measure(number=theme_measure.number)
        lowered = {"E": "E-", "A": "A-", "B": "B-"}
        for n in theme_measure.notes:
            name = n.pitch.step
            new_name = lowered.get(name, name)
            new_pitch = new_name + str(n.pitch.octave)
            m.append(note.Note(new_pitch, quarterLength=n.quarterLength))
        result.append(m)
    return result


def apply_variation(theme_part, func):
    """高阶函数：对主题应用任意变奏函数。"""
    return func(theme_part)


def main():
    print("第12课 变奏的多态艺术")

    theme = make_theme(number=1)
    variations = [
        ("主题", lambda x: x),
        ("装饰加花", var_ornament),
        ("节奏加密", var_rhythm),
        ("转小调", var_minor),
    ]

    # 分别导出每个变奏
    for name, func in variations:
        part = make_part(name=name)
        for m in apply_variation(copy.deepcopy(theme), func).getElementsByClass(stream.Measure):
            part.append(m)
        renumber_measures(part)
        # 调号写入第一小节，避免 Part 级插入产生 measure 0
        part.getElementsByClass(stream.Measure)[0].insert(0, key.Key("C"))
        safe_name = name.replace(" ", "_")

        score = make_score(title=f"第12课 {name}")
        score.append(part)
        score.write("musicxml", fp=os.path.join(OUTPUT_DIR, f"lesson12_{safe_name}.xml"))
        print(f"已导出：lesson12_{safe_name}.xml")

    # 组合为完整变奏曲：主题 -> 变奏1 -> 变奏2 -> 变奏3 -> 主题再现
    full = make_score(title="第12课 变奏曲全集")
    order = ["主题", "装饰加花", "节奏加密", "转小调", "主题"]
    for idx, name in enumerate(order):
        func = dict(variations)[name]
        part = make_part(name=f"{idx+1}. {name}")
        for m in apply_variation(copy.deepcopy(theme), func).getElementsByClass(stream.Measure):
            part.append(m)
        add_double_barline(part[-1])
        renumber_measures(part)
        # 调号写入第一小节，避免 Score 级插入导致 measure 0
        part.getElementsByClass(stream.Measure)[0].insert(0, key.Key("C"))
        full.append(part)
    full.write("musicxml", fp=os.path.join(OUTPUT_DIR, "lesson12_variations_full.xml"))
    print("已导出：lesson12_variations_full.xml （完整变奏曲）")


if __name__ == "__main__":
    main()
