"""
第13课 转调的空间映射
教师配套资源：音高变换、map/列表推导式、模 12 运算
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

from music21 import note, stream, key
from _score_utils import make_score, make_part


def pitch_to_midi(name):
    """音名 -> MIDI 编号。"""
    n = note.Note(name)
    return n.pitch.midi


def midi_to_pitch(midi_num):
    """MIDI 编号 -> 音名。"""
    return note.Note(midi=midi_num).pitch.nameWithOctave


def transpose_stream(a_stream, semitones):
    """对 Stream 中所有 Note 统一移调（列表推导式 / map 思想）。"""
    new_stream = stream.Stream()
    for element in a_stream.flatten().notesAndRests:
        if isinstance(element, note.Note):
            new_stream.append(element.transpose(semitones))
        else:
            new_stream.append(element)
    return new_stream


def major_to_minor(theme_stream):
    """同主音大小调转换：降 III、VI、VII 级。"""
    converted = stream.Stream()
    for element in theme_stream.flatten().notesAndRests:
        if isinstance(element, note.Note):
            step = element.pitch.step
            if step in ("E", "A", "B"):
                converted.append(element.transpose(-1))
            else:
                converted.append(element)
        else:
            converted.append(element)
    return converted


def make_theme():
    """C 大调主题。"""
    part = stream.Part()
    part.insert(0, key.Key("C"))
    pitches = ["C4", "D4", "E4", "F4", "G4", "G4", "A4", "G4",
               "F4", "F4", "E4", "E4", "D4", "D4", "C4", None]
    for p in pitches:
        if p is None:
            part.append(note.Rest(quarterLength=1))
        else:
            part.append(note.Note(p, quarterLength=1))
    return part


def main():
    print("第13课 转调的空间映射")

    # 1. 模 12 验证：八度等价
    print("\n【模 12 验证】")
    for name in ["C4", "C5", "C6"]:
        midi = pitch_to_midi(name)
        print(f"  {name} -> MIDI {midi} -> mod12 = {midi % 12}")

    theme = make_theme()

    # 2. 整体移高 2 半音（D 大调）
    d_major = transpose_stream(theme, 2)
    d_major.insert(0, key.Key("D"))
    score_d = make_score(title="第13课 移高 2 半音（D 大调）")
    score_d.append(d_major)
    score_d.write("musicxml", fp=os.path.join(OUTPUT_DIR, "lesson13_transposed_D.xml"))
    print("\n已导出：lesson13_transposed_D.xml （移高 2 半音）")

    # 3. 整体移高 5 半音（F 大调）
    f_major = transpose_stream(theme, 5)
    f_major.insert(0, key.Key("F"))
    score_f = make_score(title="第13课 移高 5 半音（F 大调）")
    score_f.append(f_major)
    score_f.write("musicxml", fp=os.path.join(OUTPUT_DIR, "lesson13_transposed_F.xml"))
    print("已导出：lesson13_transposed_F.xml （移高 5 半音）")

    # 4. C 大调 -> G 大调转调：前半段 C 大调，后半段 G 大调
    score_mod = make_score(title="第13课 C 大调转 G 大调")
    c_part = make_part(name="C 大调")
    c_part.insert(0, key.Key("C"))
    for n in ["C4", "E4", "G4", "E4", "D4", "F4", "A4", "F4"]:
        c_part.append(note.Note(n, quarterLength=1))

    g_part = make_part(name="G 大调")
    g_part.insert(0, key.Key("G"))
    for n in ["G4", "B4", "D5", "B4", "A4", "C5", "E5", "C5"]:
        g_part.append(note.Note(n, quarterLength=1))

    score_mod.append(c_part)
    score_mod.append(g_part)
    score_mod.write("musicxml", fp=os.path.join(OUTPUT_DIR, "lesson13_modulation_C_to_G.xml"))
    print("已导出：lesson13_modulation_C_to_G.xml （C 大调 -> G 大调）")

    # 5. 同主音大小调转换
    minor_theme = major_to_minor(theme)
    minor_theme.insert(0, key.Key("C", "minor"))
    score_min = make_score(title="第13课 C 大调转 c 小调")
    score_min.append(minor_theme)
    score_min.write("musicxml", fp=os.path.join(OUTPUT_DIR, "lesson13_major_to_minor.xml"))
    print("已导出：lesson13_major_to_minor.xml （C 大调 -> c 小调）")


if __name__ == "__main__":
    main()
