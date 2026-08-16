"""
第5课 乐句的封装
教师配套资源：用函数组织动机/乐句/乐段
每个段落之间用双竖线划分乐句边界
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

from music21 import note, stream, meter
from _score_utils import make_score, make_part, add_double_barline, renumber_measures


def make_motive(pitch_list, durations):
    """动机工厂：一组音高与时值构成一个动机（1 小节）。"""
    m = stream.Measure()
    for p, d in zip(pitch_list, durations):
        m.append(note.Note(p, quarterLength=d))
    return m


def phrase_verse(transpose=0):
    """主歌乐句（4 小节），可整体移调。"""
    part = stream.Part()
    part.insert(0, meter.TimeSignature("4/4"))

    m1 = make_motive(["C4", "E4", "G4", "E4"], [1, 1, 1, 1])
    m2 = make_motive(["D4", "F4", "A4", "F4"], [1, 1, 1, 1])
    m3 = make_motive(["C4", "D4", "E4", "C4"], [1, 1, 1, 1])
    m4 = make_motive(["G3", "C4", "E4", "C4"], [1, 1, 1, 1])

    for m in [m1, m2, m3, m4]:
        m.transpose(transpose, inPlace=True)
        part.append(m)
    # 乐句末尾双竖线
    add_double_barline(m4)
    return part


def phrase_chorus(transpose=0):
    """副歌乐句（4 小节）。"""
    part = stream.Part()
    part.insert(0, meter.TimeSignature("4/4"))

    data = [
        (["C4", "C4", "E4", "G4"], [1, 1, 1, 1]),
        (["G4", "F4", "E4", "D4"], [1, 1, 1, 1]),
        (["C4", "E4", "G4", "C5"], [1, 1, 1, 1]),
        (["G4", "E4", "D4", "C4"], [1, 1, 1, 1]),
    ]
    for pitches, durs in data:
        m = make_motive(pitches, durs)
        m.transpose(transpose, inPlace=True)
        part.append(m)
    # 乐句末尾双竖线
    add_double_barline(part[-1])
    return part


def phrase_bridge(transpose=0):
    """桥段乐句（4 小节）。"""
    part = stream.Part()
    part.insert(0, meter.TimeSignature("4/4"))

    data = [
        (["F4", "A4", "C5", "A4"], [1, 1, 1, 1]),
        (["E4", "G4", "B4", "G4"], [1, 1, 1, 1]),
        (["D4", "F4", "A4", "F4"], [1, 1, 1, 1]),
        (["G3", "B3", "D4", "G4"], [1, 1, 1, 1]),
    ]
    for pitches, durs in data:
        m = make_motive(pitches, durs)
        m.transpose(transpose, inPlace=True)
        part.append(m)
    return part


def main():
    print("第5课 乐句的封装")

    # 组合完整歌曲：主歌 + 副歌 + 主歌 + 副歌 + 桥段 + 副歌
    score = make_score(title="第5课 乐句的封装：主歌-副歌-桥段")
    song_part = make_part(name="主旋律")

    sections = [
        phrase_verse(),
        phrase_chorus(),
        phrase_verse(),
        phrase_chorus(transpose=0),
        phrase_bridge(),
        phrase_chorus(transpose=0),
    ]

    for section in sections:
        for m in section.getElementsByClass(stream.Measure):
            song_part.append(m)

    # 小节顺序重新编号
    renumber_measures(song_part)

    score.append(song_part)
    score.write("musicxml", fp=os.path.join(OUTPUT_DIR, "lesson05_phrase_functions.xml"))
    print("已导出：lesson05_phrase_functions.xml")
    print("歌曲结构：主歌-副歌-主歌-副歌-桥段-副歌")


if __name__ == "__main__":
    main()
