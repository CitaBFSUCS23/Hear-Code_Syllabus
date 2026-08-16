"""
第1课 音高的数字本质
教师配套资源：演示 MIDI、频率与 Note 对象模型
运行后导出 MusicXML 乐谱
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

from music21 import note, stream
from _score_utils import make_score
import math


def midi_to_freq(midi_number: float) -> float:
    """将 MIDI 编号转换为频率（十二平均律，A4=440Hz，MIDI 69）。"""
    return 440.0 * (2 ** ((midi_number - 69) / 12))


def main():
    print("=" * 50)
    print("第1课 音高的数字本质")
    print("=" * 50)

    # 1. 创建四个音符对象并观察三重数字表达
    pitch_names = ["C4", "E4", "G4", "C5"]
    notes = [note.Note(p) for p in pitch_names]

    print("\n【三重数字表达】")
    print(f"{'音名':<8}{'MIDI':<8}{'music21频率':<18}{'公式计算频率':<18}")
    for n in notes:
        p = n.pitch
        calc_freq = midi_to_freq(p.midi)
        print(f"{p.nameWithOctave:<8}{p.midi:<8}{p.frequency:<18.6f}{calc_freq:<18.6f}")

    # 2. 验证八度关系：MIDI 相差 12，频率比为 2:1
    c4 = note.Note("C4")
    c5 = note.Note("C5")
    ratio = c5.pitch.frequency / c4.pitch.frequency
    print(f"\n【八度验证】C5/C4 频率比 = {ratio:.6f} （接近 2.0）")

    # 3. 纯五度频率比验证
    g4 = note.Note("G4")
    perfect_fifth_ratio = g4.pitch.frequency / c4.pitch.frequency
    print(f"【纯五度验证】G4/C4 频率比 = {perfect_fifth_ratio:.6f} （接近 3:2 = 1.5）")

    # 4. 用 Stream 组合一段 C 大调音阶旋律（四分+二分音符）
    melody = stream.Part()
    scale_pitches = ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"]
    durations = [1, 1, 2, 1, 1, 1, 1, 2]  # 以四分音符为单位
    for p, d in zip(scale_pitches, durations):
        melody.append(note.Note(p, quarterLength=d))

    score = make_score(title="第1课 音高的数字本质")
    score.append(melody)

    # 导出 MusicXML
    xml_path = os.path.join(OUTPUT_DIR, "lesson01_pitch_numbers.xml")
    score.write("musicxml", fp=xml_path)
    print(f"\n【乐谱已导出】{xml_path}")
    print("可导入 MuseScore / Sibelius / Finale 查看并播放。")


if __name__ == "__main__":
    main()
