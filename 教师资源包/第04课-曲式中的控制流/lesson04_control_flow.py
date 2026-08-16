"""
第4课 曲式中的控制流
教师配套资源：反复、跳房子（Volta）、D.C.、D.S.、Coda 等标准跳跃结构
本课生成 4 个独立乐谱，小节编号均从 1 开始连续递增。
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

from music21 import note, stream, meter
from _score_utils import (
    make_score, make_part, add_repeat_start, add_repeat_end,
    add_volta_bracket, add_da_capo, add_dal_segno, add_fine,
    add_text_expression, add_double_barline, add_final_barline
)


def make_A_section(start_measure=1):
    """A 段：4 小节旋律。"""
    data = [
        [("C4", 1), ("D4", 1), ("E4", 1), ("F4", 1)],
        [("G4", 2), ("G4", 1), ("A4", 1)],
        [("G4", 0.5), ("F4", 0.5), ("E4", 1), ("D4", 1)],
        [("C4", 2), ("G3", 2)],
    ]
    measures = []
    for i, notes_data in enumerate(data, start=start_measure):
        m = stream.Measure(number=i)
        if i == start_measure:
            m.timeSignature = meter.TimeSignature("4/4")
        for p, ql in notes_data:
            m.append(note.Note(p, quarterLength=ql))
        measures.append(m)
    return measures


def make_B_section(start_measure=5):
    """B 段：4 小节对比旋律。"""
    data = [
        [("F4", 1), ("A4", 1), ("C5", 1), ("A4", 1)],
        [("G4", 1), ("B4", 1), ("D5", 1), ("B4", 1)],
        [("E4", 1), ("G4", 1), ("C5", 1), ("G4", 1)],
        [("D4", 1), ("F4", 1), ("A4", 1), ("F4", 1)],
    ]
    measures = []
    for i, notes_data in enumerate(data, start=start_measure):
        m = stream.Measure(number=i)
        for p, ql in notes_data:
            m.append(note.Note(p, quarterLength=ql))
        measures.append(m)
    return measures


def make_C_closing(start_measure=9, final_note=("C4", 4)):
    """C 段：2 小节收束。"""
    data = [
        [("E4", 1), ("G4", 1), ("C5", 1), ("G4", 1)],
        [final_note],
    ]
    measures = []
    for i, notes_data in enumerate(data, start=start_measure):
        m = stream.Measure(number=i)
        for p, ql in notes_data:
            m.append(note.Note(p, quarterLength=ql))
        measures.append(m)
    return measures


def example_volta():
    """示例 1：反复 + 第一/第二结尾（跳房子）。

    演奏路径：A(1-4) → 第一结尾(5) → 反复 A(1-4) → 跳过第一结尾 → 第二结尾(6) → 尾声(7-8)。
    反复返回记号放在第一结尾末尾，第二结尾前方，这样第一次演奏到第一结尾后返回 A，
    第二次直接跳过第一结尾进入第二结尾。
    """
    score = make_score(title="第4课 反复与跳房子")
    part = make_part(name="旋律")

    a_measures = make_A_section(start_measure=1)
    add_repeat_start(a_measures[0])
    for m in a_measures:
        part.append(m)

    ending1 = stream.Measure(number=5)
    ending1.append(note.Note("C4", quarterLength=1))
    ending1.append(note.Note("E4", quarterLength=1))
    ending1.append(note.Note("G4", quarterLength=2))
    add_repeat_end(ending1)  # 反复返回记号在第一结尾末尾
    part.append(ending1)
    add_volta_bracket(part, ending1, number=1)

    ending2 = stream.Measure(number=6)
    ending2.append(note.Note("C4", quarterLength=0.5))
    ending2.append(note.Note("D4", quarterLength=0.5))
    ending2.append(note.Note("E4", quarterLength=0.5))
    ending2.append(note.Note("F4", quarterLength=0.5))
    ending2.append(note.Note("G4", quarterLength=1))
    ending2.append(note.Note("C5", quarterLength=1))
    part.append(ending2)
    add_volta_bracket(part, ending2, number=2)
    add_double_barline(ending2)

    # 跳房子之后追加 2 小节尾声，让结构更完整
    c_measures = make_C_closing(start_measure=7, final_note=("C4", 4))
    add_final_barline(c_measures[-1])
    for m in c_measures:
        part.append(m)

    score.append(part)
    return score


def example_dc_al_fine():
    """示例 2：D.C. al Fine。

    演奏路径：A(1-4) → B(5-8) → 过渡(9-10) → D.C. 回到 A(1-4) → Fine 结束。
    """
    score = make_score(title="第4课 D.C. al Fine")
    part = make_part(name="旋律")

    # A 段
    a_measures = make_A_section(start_measure=1)
    for m in a_measures:
        part.append(m)
    add_double_barline(part[-1])
    add_fine(part[-1])  # A 段末尾标记 Fine

    # B 段
    b_measures = make_B_section(start_measure=5)
    for m in b_measures:
        part.append(m)
    add_double_barline(part[-1])

    # 过渡段
    transition = stream.Measure(number=9)
    transition.append(note.Note("E4", quarterLength=1))
    transition.append(note.Note("G4", quarterLength=1))
    transition.append(note.Note("C5", quarterLength=1))
    transition.append(note.Note("G4", quarterLength=1))
    part.append(transition)

    # D.C. al Fine：回到开头，演奏到 Fine 处结束
    last = stream.Measure(number=10)
    last.append(note.Note("C4", quarterLength=2))
    last.append(note.Note("G3", quarterLength=2))
    add_da_capo(last, "D.C. al Fine")
    part.append(last)

    score.append(part)
    return score


def example_ds_al_coda():
    """示例 3：D.S. al Coda。

    演奏路径：Intro(1-2) → A(3-6, 含 Segno) → B(7-10) →
             桥(11-12, D.S. al Coda & To Coda) → 回到 Segno(3) →
             演奏至 To Coda → Coda(13-14)。
    """
    score = make_score(title="第4课 D.S. al Coda")
    part = make_part(name="旋律")

    # 引子（Intro）
    intro1 = stream.Measure(number=1)
    intro1.timeSignature = meter.TimeSignature("4/4")
    intro1.append(note.Note("C4", quarterLength=1))
    intro1.append(note.Note("E4", quarterLength=1))
    intro1.append(note.Note("G4", quarterLength=2))
    part.append(intro1)

    intro2 = stream.Measure(number=2)
    intro2.append(note.Note("F4", quarterLength=1))
    intro2.append(note.Note("A4", quarterLength=1))
    intro2.append(note.Note("C5", quarterLength=2))
    add_double_barline(intro2)
    part.append(intro2)

    # A 段（含 Segno）
    a_measures = make_A_section(start_measure=3)
    add_text_expression(a_measures[0], "Segno")  # 第 3 小节标记 Segno
    for m in a_measures:
        part.append(m)
    add_double_barline(part[-1])

    # B 段
    b_measures = make_B_section(start_measure=7)
    for m in b_measures:
        part.append(m)
    add_double_barline(part[-1])

    # 桥段：包含 D.S. al Coda 与 To Coda
    bridge1 = stream.Measure(number=11)
    bridge1.append(note.Note("E4", quarterLength=1))
    bridge1.append(note.Note("G4", quarterLength=1))
    bridge1.append(note.Note("C5", quarterLength=1))
    bridge1.append(note.Note("G4", quarterLength=1))
    part.append(bridge1)

    bridge2 = stream.Measure(number=12)
    bridge2.append(note.Note("G4", quarterLength=2))
    bridge2.append(note.Note("C4", quarterLength=2))
    add_dal_segno(bridge2, "D.S. al Coda")
    add_text_expression(bridge2, "To Coda")
    part.append(bridge2)

    # Coda 段落
    coda1 = stream.Measure(number=13)
    coda1.append(note.Note("C5", quarterLength=1))
    coda1.append(note.Note("G4", quarterLength=1))
    coda1.append(note.Note("E4", quarterLength=1))
    coda1.append(note.Note("C4", quarterLength=1))
    add_text_expression(coda1, "Coda")
    part.append(coda1)

    coda2 = stream.Measure(number=14)
    coda2.append(note.Note("C4", quarterLength=4))
    add_final_barline(coda2)
    part.append(coda2)

    score.append(part)
    return score


def example_dc_al_coda():
    """示例 4：D.C. al Coda。

    演奏路径：A(1-4, 含 To Coda) → B(5-8) → D.C. al Coda →
             从头演奏到 To Coda → Coda(9-10)。
    """
    score = make_score(title="第4课 D.C. al Coda")
    part = make_part(name="旋律")

    # A 段：末尾标记 To Coda
    a_measures = make_A_section(start_measure=1)
    add_text_expression(a_measures[-1], "To Coda")
    for m in a_measures:
        part.append(m)
    add_double_barline(part[-1])

    # B 段
    b_measures = make_B_section(start_measure=5)
    for m in b_measures:
        part.append(m)
    add_double_barline(part[-1])

    # D.C. al Coda
    dc = stream.Measure(number=9)
    dc.append(note.Note("G4", quarterLength=2))
    dc.append(note.Note("C4", quarterLength=2))
    add_da_capo(dc, "D.C. al Coda")
    part.append(dc)

    # Coda 段落
    coda1 = stream.Measure(number=10)
    coda1.append(note.Note("C5", quarterLength=1))
    coda1.append(note.Note("G4", quarterLength=1))
    coda1.append(note.Note("E4", quarterLength=1))
    coda1.append(note.Note("C4", quarterLength=1))
    add_text_expression(coda1, "Coda")
    part.append(coda1)

    coda2 = stream.Measure(number=11)
    coda2.append(note.Note("C4", quarterLength=4))
    add_final_barline(coda2)
    part.append(coda2)

    score.append(part)
    return score


def main():
    print("第4课 曲式中的控制流")

    # 示例 1：跳房子
    score1 = example_volta()
    score1.write("musicxml", fp=os.path.join(OUTPUT_DIR, "lesson04_control_flow.xml"))
    print("已导出：lesson04_control_flow.xml （反复 + 跳房子，1-8 小节）")

    # 示例 2：D.C. al Fine
    score2 = example_dc_al_fine()
    score2.write("musicxml", fp=os.path.join(OUTPUT_DIR, "lesson04_dc_al_fine.xml"))
    print("已导出：lesson04_dc_al_fine.xml （D.C. al Fine，1-10 小节）")

    # 示例 3：D.S. al Coda
    score3 = example_ds_al_coda()
    score3.write("musicxml", fp=os.path.join(OUTPUT_DIR, "lesson04_ds_al_coda.xml"))
    print("已导出：lesson04_ds_al_coda.xml （D.S. al Coda，1-14 小节）")

    # 示例 4：D.C. al Coda
    score4 = example_dc_al_coda()
    score4.write("musicxml", fp=os.path.join(OUTPUT_DIR, "lesson04_dc_al_coda.xml"))
    print("已导出：lesson04_dc_al_coda.xml （D.C. al Coda，1-11 小节）")

    # 打印演奏路径说明
    print("\n【四种跳跃结构演奏路径】")
    print("  1. 反复+跳房子：A | 1. | 反复 | A | 2. | 尾声 ||")
    print("  2. D.C. al Fine：A -> B -> 过渡 -> 回到 A -> Fine")
    print("  3. D.S. al Coda：Intro -> A(Segno) -> B -> 桥 -> 回 Segno -> To Coda -> Coda")
    print("  4. D.C. al Coda：A(To Coda) -> B -> D.C. -> 到 To Coda -> Coda")


if __name__ == "__main__":
    main()
