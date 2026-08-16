"""
第10课 模进的迭代算法
教师配套资源：动机发展与循环嵌套
生成上行模进、下行模进、倒影片段
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

import copy
from music21 import note, stream, key, meter
from _score_utils import make_score, make_part, add_double_barline, renumber_measures


def make_motive(number=1):
    """2 小节动机：C-E-G-E。"""
    m = stream.Measure(number=number)
    m.timeSignature = meter.TimeSignature("4/4")
    m.append(note.Note("C4", quarterLength=1))
    m.append(note.Note("E4", quarterLength=1))
    m.append(note.Note("G4", quarterLength=1))
    m.append(note.Note("E4", quarterLength=1))
    m.append(note.Note("D4", quarterLength=1))
    m.append(note.Note("F4", quarterLength=1))
    m.append(note.Note("A4", quarterLength=1))
    m.append(note.Note("F4", quarterLength=1))
    return m


def make_sequence(motive, steps, semitone_step, in_key=True, key_sig=None):
    """用迭代生成模进。

    Args:
        motive: 原始动机（Measure）
        steps: 重复次数
        semitone_step: 每次移高多少半音
        in_key: 是否守调（超出调式音阶时做调整）
        key_sig: 调号，用于守调处理
    """
    seq = stream.Part()
    for i in range(steps):
        transposed = motive.transpose(i * semitone_step)
        if in_key and key_sig:
            # 简单守调：将超过调式范围的音拉回八度内
            for n in transposed.notes:
                while n.pitch.midi > 79:
                    n.transpose(-12, inPlace=True)
                while n.pitch.midi < 55:
                    n.transpose(12, inPlace=True)
        seq.append(transposed)
    renumber_measures(seq)
    # 调号写入第一小节，避免 Part 级插入产生 measure 0
    if key_sig:
        first = seq.getElementsByClass(stream.Measure).first()
        if first is not None:
            first.insert(0, copy.deepcopy(key_sig))
    return seq


def invert_motive(motive):
    """倒影：以 C4 为轴，音程方向反转。"""
    inverted = stream.Measure()
    inverted.timeSignature = motive.timeSignature
    first_pitch = motive.notes[0].pitch.midi
    for n in motive.notes:
        offset = n.pitch.midi - first_pitch
        inverted_pitch = first_pitch - offset
        inverted.append(note.Note(midi=inverted_pitch, quarterLength=n.quarterLength))
    return inverted


def main():
    print("第10课 模进的迭代算法")

    motive = make_motive(number=1)
    key_sig = key.Key("C")

    # 1. 上行严格模进（每次 +2 半音，重复 4 次）
    up_seq = make_sequence(motive, steps=4, semitone_step=2, in_key=False, key_sig=key_sig)
    score_up = make_score(title="第10课 上行严格模进")
    score_up.append(up_seq)
    score_up.write("musicxml", fp=os.path.join(OUTPUT_DIR, "lesson10_sequence_up.xml"))
    print("已导出：lesson10_sequence_up.xml （上行严格模进）")

    # 2. 下行模进（每次 -2 半音）
    down_seq = make_sequence(motive, steps=4, semitone_step=-2, in_key=False, key_sig=key_sig)
    score_down = make_score(title="第10课 下行模进")
    score_down.append(down_seq)
    score_down.write("musicxml", fp=os.path.join(OUTPUT_DIR, "lesson10_sequence_down.xml"))
    print("已导出：lesson10_sequence_down.xml （下行模进）")

    # 3. 守调模进（C 大调内）
    diatonic_seq = make_sequence(motive, steps=4, semitone_step=2, in_key=True, key_sig=key_sig)
    score_dia = make_score(title="第10课 守调模进")
    score_dia.append(diatonic_seq)
    score_dia.write("musicxml", fp=os.path.join(OUTPUT_DIR, "lesson10_sequence_diatonic.xml"))
    print("已导出：lesson10_sequence_diatonic.xml （守调模进）")

    # 4. 倒影
    inv = invert_motive(motive)
    inv_part = make_part(name="旋律")
    inv_part.append(motive)
    add_double_barline(motive)
    inv_part.append(inv)
    renumber_measures(inv_part)
    # 调号写入第一小节
    inv_part.getElementsByClass(stream.Measure)[0].insert(0, key.Key("C"))

    score_inv = make_score(title="第10课 动机与倒影")
    score_inv.append(inv_part)
    score_inv.write("musicxml", fp=os.path.join(OUTPUT_DIR, "lesson10_inversion.xml"))
    print("已导出：lesson10_inversion.xml （动机 + 倒影）")


if __name__ == "__main__":
    main()
