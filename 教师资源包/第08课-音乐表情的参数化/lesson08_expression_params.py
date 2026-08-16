"""
第8课 音乐表情的参数化
教师配套资源：力度、速度、演奏法与函数参数
生成同一旋律的三种情绪版本 + 渐强片段
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

from music21 import note, stream, dynamics, tempo, articulations, meter
from _score_utils import make_score, make_part, renumber_measures


def make_theme_notes():
    """基础主题音符序列（8 小节，每小节 4 拍）。"""
    pitches = [
        "C4", "D4", "E4", "C4",
        "C4", "D4", "E4", "C4",
        "E4", "F4", "G4", None,
        "E4", "F4", "G4", None,
        "G4", "A4", "G4", "F4", "E4", "C4", None, None,
        "G4", "F4", "E4", "D4", "C4", None, None, None,
    ]
    return [note.Rest(quarterLength=1) if p is None else note.Note(p, quarterLength=1) for p in pitches]


def emotion_version(dyn, bpm, staccato=False):
    """参数化情绪版本：力度、速度、是否断奏。"""
    part = make_part(name=f"情绪 {dyn}")
    part.append(tempo.MetronomeMark(number=bpm))
    part.append(dynamics.Dynamic(dyn))

    notes = make_theme_notes()
    measures = []
    beats_per_measure = 4.0
    current = stream.Measure(number=1)
    current.timeSignature = meter.TimeSignature("4/4")
    current_len = 0.0
    measure_num = 1

    for n in notes:
        ql = n.quarterLength
        if current_len + ql > beats_per_measure + 1e-9 and current_len > 0:
            measures.append(current)
            measure_num += 1
            current = stream.Measure(number=measure_num)
            current.timeSignature = meter.TimeSignature("4/4")
            current_len = 0.0
        if staccato and isinstance(n, note.Note):
            n.articulations.append(articulations.Staccato())
        current.append(n)
        current_len += ql
    measures.append(current)

    for m in measures:
        part.append(m)
    return part


def crescendo_fragment():
    """渐强片段：力度从 p 逐步增加到 f（4 小节）。"""
    part = make_part(name="渐强")
    part.append(tempo.MetronomeMark(number=90))

    levels = ["p", "mp", "mf", "f"]
    pitches = [
        ["C4", "D4", "E4", "F4"],
        ["G4", "A4", "B4", "C5"],
        ["D5", "C5", "B4", "A4"],
        ["G4", "F4", "E4", "C4"],
    ]
    for i, (level, grp) in enumerate(zip(levels, pitches), start=1):
        m = stream.Measure(number=i)
        m.append(dynamics.Dynamic(level))
        for p in grp:
            m.append(note.Note(p, quarterLength=1))
        part.append(m)
    return part


def accelerando_fragment():
    """渐快片段：速度从 60 BPM 逐步增加到 120 BPM（4 小节）。"""
    part = make_part(name="渐快")
    bpms = [60, 80, 100, 120]
    pitches = [
        ["C4", "E4", "G4", "C5"],
        ["C5", "G4", "E4", "C4"],
        ["D4", "F4", "A4", "D5"],
        ["D5", "A4", "F4", "D4"],
    ]
    for i, (bpm, grp) in enumerate(zip(bpms, pitches), start=1):
        m = stream.Measure(number=i)
        m.append(tempo.MetronomeMark(number=bpm))
        for p in grp:
            m.append(note.Note(p, quarterLength=1))
        part.append(m)
    return part


def main():
    print("第8课 音乐表情的参数化")

    # 轻柔版
    soft = emotion_version("p", 60, staccato=False)
    score_soft = make_score(title="第8课 轻柔版 (p / Largo)")
    score_soft.append(soft)
    score_soft.write("musicxml", fp=os.path.join(OUTPUT_DIR, "lesson08_soft.xml"))
    print("已导出：lesson08_soft.xml （p + Andante + legato）")

    # 激昂版
    strong = emotion_version("f", 132, staccato=True)
    score_strong = make_score(title="第8课 激昂版 (f / Allegro)")
    score_strong.append(strong)
    score_strong.write("musicxml", fp=os.path.join(OUTPUT_DIR, "lesson08_strong.xml"))
    print("已导出：lesson08_strong.xml （f + Allegro + staccato）")

    # 神秘版
    mysterious = emotion_version("pp", 50, staccato=False)
    score_myst = make_score(title="第8课 神秘版 (pp / Largo)")
    score_myst.append(mysterious)
    score_myst.write("musicxml", fp=os.path.join(OUTPUT_DIR, "lesson08_mysterious.xml"))
    print("已导出：lesson08_mysterious.xml （pp + Largo）")

    # 渐强
    cres = crescendo_fragment()
    score_cres = make_score(title="第8课 渐强 (p -> f)")
    score_cres.append(cres)
    score_cres.write("musicxml", fp=os.path.join(OUTPUT_DIR, "lesson08_crescendo.xml"))
    print("已导出：lesson08_crescendo.xml")

    # 渐快
    acc = accelerando_fragment()
    score_acc = make_score(title="第8课 渐快 (60 -> 120 BPM)")
    score_acc.append(acc)
    score_acc.write("musicxml", fp=os.path.join(OUTPUT_DIR, "lesson08_accelerando.xml"))
    print("已导出：lesson08_accelerando.xml")


if __name__ == "__main__":
    main()
