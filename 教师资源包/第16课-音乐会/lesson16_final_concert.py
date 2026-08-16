"""
第16课 音乐会
教师配套资源：综合运用全课程概念创作一首完整作品
包含：曲式结构、转调、模进、和弦伴奏、表情参数、多乐器配器

本谱结构（共 14 小节）：
  第 1-2 小节：引子（钢琴分解和弦）
  第 3-6 小节：A 段（长笛，C 大调）
  第 7-10 小节：B 段（小提琴，G 大调，新页开始）
  第 11-14 小节：A 段再现（长笛，C 大调）
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

from music21 import note, stream, chord as chord_module, instrument, dynamics, tempo, key, meter, layout
from _score_utils import make_score, make_part, add_double_barline, add_final_barline


def build_empty_measure(number, beats=4):
    """生成指定小节的休止符小节。"""
    m = stream.Measure(number=number)
    m.timeSignature = meter.TimeSignature("4/4")
    m.append(note.Rest(quarterLength=beats))
    return m


def main():
    print("第16课 音乐会")

    score = make_score(title="第16课 音乐会")
    score.insert(0, tempo.MetronomeMark(number=112))
    score.insert(0, key.Key("C"))

    # 三个声部，统一 14 小节
    flute_part = make_part(name="长笛", instrument_obj=instrument.Flute())
    violin_part = make_part(name="小提琴", instrument_obj=instrument.Violin())
    piano_part = make_part(name="钢琴", instrument_obj=instrument.Piano())

    # ===== 第 1-2 小节：引子（钢琴分解和弦） =====
    intro_pitches = ["C4", "E4", "G4", "E4", "A3", "E4", "A4", "E4"]
    for i in range(2):
        m_piano = stream.Measure(number=i + 1)
        m_piano.timeSignature = meter.TimeSignature("4/4")
        for p in intro_pitches:
            m_piano.append(note.Note(p, quarterLength=0.5))
        piano_part.append(m_piano)

        flute_part.append(build_empty_measure(i + 1))
        violin_part.append(build_empty_measure(i + 1))

    # ===== 第 3-6 小节：A 段（长笛 + 钢琴柱式和弦） =====
    a_pitches = ["C5", "D5", "E5", "C5", "G5", "E5", "D5", "C5",
                 "A4", "C5", "E5", "D5", "C5", "B4", "A4", "G4"]
    a_chords = [
        ("C3", "E3", "G3"), ("C3", "E3", "G3"),
        ("F2", "A2", "C3"), ("F2", "A2", "C3"),
    ]
    for i in range(4):
        measure_num = 3 + i

        m_flute = stream.Measure(number=measure_num)
        m_flute.timeSignature = meter.TimeSignature("4/4")
        for p in a_pitches[i * 4:(i + 1) * 4]:
            m_flute.append(note.Note(p, quarterLength=1))
        flute_part.append(m_flute)

        m_piano = stream.Measure(number=measure_num)
        m_piano.timeSignature = meter.TimeSignature("4/4")
        m_piano.append(chord_module.Chord(a_chords[i], quarterLength=4))
        piano_part.append(m_piano)

        violin_part.append(build_empty_measure(measure_num))

    add_double_barline(flute_part[-1])

    # ===== 第 7-10 小节：B 段（小提琴 + 钢琴柱式和弦，G 大调，新页） =====
    b_pitches = ["G5", "A5", "B5", "G5", "D6", "B5", "A5", "G5",
                 "F#5", "A5", "C6", "B5", "A5", "G5", "F#5", "G5"]
    b_chords = [
        ("G2", "B2", "D3"), ("G2", "B2", "D3"),
        ("D3", "F#3", "A3"), ("D3", "F#3", "A3"),
    ]
    for i in range(4):
        measure_num = 7 + i

        m_violin = stream.Measure(number=measure_num)
        m_violin.timeSignature = meter.TimeSignature("4/4")
        if i == 0:
            m_violin.insert(0, layout.PageLayout(isNew=True))
            m_violin.insert(0, key.Key("G"))
        for p in b_pitches[i * 4:(i + 1) * 4]:
            m_violin.append(note.Note(p, quarterLength=1))
        violin_part.append(m_violin)

        m_piano = stream.Measure(number=measure_num)
        m_piano.timeSignature = meter.TimeSignature("4/4")
        if i == 0:
            m_piano.insert(0, layout.PageLayout(isNew=True))
            m_piano.insert(0, key.Key("G"))
        m_piano.append(chord_module.Chord(b_chords[i], quarterLength=4))
        piano_part.append(m_piano)

        flute_part.append(build_empty_measure(measure_num))

    add_double_barline(violin_part[-1])

    # ===== 第 11-14 小节：A 段再现（长笛 + 钢琴柱式和弦，回到 C 大调） =====
    a_return_chords = [
        ("C3", "E3", "G3"), ("C3", "E3", "G3"),
        ("G2", "B2", "D3"), ("C3", "E3", "G3"),
    ]
    for i in range(4):
        measure_num = 11 + i

        m_flute = stream.Measure(number=measure_num)
        m_flute.timeSignature = meter.TimeSignature("4/4")
        if i == 0:
            m_flute.insert(0, key.Key("C"))
        for p in a_pitches[i * 4:(i + 1) * 4]:
            m_flute.append(note.Note(p, quarterLength=1))
        flute_part.append(m_flute)

        m_piano = stream.Measure(number=measure_num)
        m_piano.timeSignature = meter.TimeSignature("4/4")
        if i == 0:
            m_piano.insert(0, key.Key("C"))
        m_piano.append(chord_module.Chord(a_return_chords[i], quarterLength=4))
        piano_part.append(m_piano)

        violin_part.append(build_empty_measure(measure_num))

    add_final_barline(flute_part[-1])

    score.append(flute_part)
    score.append(violin_part)
    score.append(piano_part)

    score.write("musicxml", fp=os.path.join(OUTPUT_DIR, "lesson16_final_concert.xml"))
    print("已导出：lesson16_final_concert.xml")
    print("\n作品结构：引子(1-2) - A段(3-6) - B段(7-10, G大调, 新页) - A段再现(11-14)")
    print("综合运用：曲式结构、移调/转调、和声伴奏、表情参数、多乐器配器")


if __name__ == "__main__":
    main()
