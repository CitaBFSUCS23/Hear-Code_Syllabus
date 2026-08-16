"""
第9课 和弦的数据结构
教师配套资源：三和弦/七和弦的字典定义与 I-IV-V-I 和弦进行
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

from music21 import note, stream, chord, key
from _score_utils import make_score, make_part


# 和弦类型定义：以根音为 0 的半音偏移集合
CHORD_TYPES = {
    "major": [0, 4, 7],
    "minor": [0, 3, 7],
    "diminished": [0, 3, 6],
    "augmented": [0, 4, 8],
    "dominant7": [0, 4, 7, 10],
    "major7": [0, 4, 7, 11],
    "minor7": [0, 3, 7, 10],
}


def make_chord(root_name, chord_type, duration=2):
    """根据根音名字符串与和弦类型生成 music21 Chord。"""
    root_note = note.Note(root_name)
    root_midi = root_note.pitch.midi
    intervals = CHORD_TYPES[chord_type]
    pitches = [root_midi + i for i in intervals]
    return chord.Chord(pitches, quarterLength=duration)


def analyze_chord(c):
    """简单分析和弦性质。"""
    info = {
        "pitches": [str(p) for p in c.pitches],
        "is_major_triad": c.isMajorTriad(),
        "is_minor_triad": c.isMinorTriad(),
        "inversion": c.inversion(),
    }
    return info


def main():
    print("第9课 和弦的数据结构")
    print("\n【和弦类型字典】")
    for name, intervals in CHORD_TYPES.items():
        print(f"  {name}: {intervals}")

    # 1. 生成并分析若干和弦
    test_chords = [
        ("C4", "major"),
        ("A3", "minor"),
        ("B3", "diminished"),
        ("G3", "dominant7"),
    ]
    print("\n【和弦分析】")
    for root, ctype in test_chords:
        c = make_chord(root, ctype)
        print(f"  {root} {ctype}: {analyze_chord(c)}")

    # 2. C 大调 I-IV-V-I 柱式和弦进行（每小节一个和弦）
    score = make_score(title="第9课 I-IV-V-I 柱式和弦进行")
    score.insert(0, key.Key("C"))

    progression_part = make_part(name="和弦")
    progression = [
        ("C3", "major"),    # I
        ("F3", "major"),    # IV
        ("G3", "major"),    # V
        ("C3", "major"),    # I
    ]
    for root, ctype in progression:
        c = make_chord(root, ctype, duration=4)
        progression_part.append(c)
    score.append(progression_part)
    score.write("musicxml", fp=os.path.join(OUTPUT_DIR, "lesson09_chord_progression.xml"))
    print("\n已导出：lesson09_chord_progression.xml （I-IV-V-I 柱式和弦）")

    # 3. 同一旋律配 I-IV-V-I 分解和弦伴奏
    score2 = make_score(title="第9课 旋律与和弦伴奏")
    score2.insert(0, key.Key("C"))

    melody_part = make_part(name="旋律")
    melody_pitches = ["C4", "E4", "G4", "E4", "F4", "A4", "G4", "B4", "C5", "G4", "E4", "C4"]
    for p in melody_pitches:
        melody_part.append(note.Note(p, quarterLength=1))

    accompaniment_part = make_part(name="伴奏")
    # 12 拍的旋律，伴奏用 4 个和弦、每个持续 3 拍（I-IV-V-I）
    accomp_progression = [
        ("C3", "E3", "G3"),    # I
        ("F3", "A3", "C4"),    # IV
        ("G3", "B3", "D4"),    # V
        ("C3", "E3", "G3"),    # I
    ]
    for grp in accomp_progression:
        accompaniment_part.append(chord.Chord(grp, quarterLength=3))

    score2.append(melody_part)
    score2.append(accompaniment_part)
    score2.write("musicxml", fp=os.path.join(OUTPUT_DIR, "lesson09_melody_with_chords.xml"))
    print("已导出：lesson09_melody_with_chords.xml （旋律+分解和弦伴奏）")


if __name__ == "__main__":
    main()
