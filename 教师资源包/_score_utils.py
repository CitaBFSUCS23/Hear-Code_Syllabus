"""
教师资源包共享工具：生成更规范的音乐记谱
用法：在每个 lesson 脚本顶部加入
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from _score_utils import make_score, add_metadata, add_double_barline, ...
"""
import os
from music21 import (
    stream, metadata, bar, spanner, expressions, layout,
    instrument, tempo, dynamics, key
)


def add_metadata(score, title, composer="听声译码"):
    """为 Score 添加标题与作曲者，避免导出为 'music21 fragment'。"""
    score.insert(0, metadata.Metadata(title=title, composer=composer))


def make_score(title, composer="听声译码"):
    """创建带标题的 Score。"""
    s = stream.Score()
    add_metadata(s, title, composer)
    return s


def make_part(name=None, instrument_obj=None, clef=None):
    """创建命名的 Part，便于在总谱中识别声部。"""
    p = stream.Part()
    if name:
        p.partName = name
    if instrument_obj is not None:
        p.insert(0, instrument_obj)
    if clef is not None:
        p.insert(0, clef)
    return p


def add_double_barline(measure):
    """在指定小节末尾添加乐句双竖线（light-light）。"""
    measure.rightBarline = bar.Barline("double")


def add_final_barline(measure):
    """在指定小节末尾添加终止双竖线（light-heavy）。"""
    measure.rightBarline = bar.Barline("final")


def add_repeat_start(measure):
    """在指定小节开头添加反复起点。"""
    measure.leftBarline = bar.Repeat(direction="start")


def add_repeat_end(measure):
    """在指定小节末尾添加反复终点。"""
    measure.rightBarline = bar.Repeat(direction="end")


def add_volta_bracket(part, measures, number):
    """为第一/第二结尾添加跳房子（Volta）括号。

    Args:
        part: 包含小节的 Part
        measures: 一个 Measure 或 Measure 列表
        number: 结尾编号（1, 2, ...）
    """
    if not isinstance(measures, (list, tuple)):
        measures = [measures]
    rb = spanner.RepeatBracket(measures, number=number)
    part.append(rb)


def add_text_expression(measure, text):
    """在小节末尾添加文字标记（如 D.C. al Fine）。"""
    measure.append(expressions.TextExpression(text))


def add_da_capo(measure, text="D.C. al Fine"):
    """添加 D.C. al Fine 标记。"""
    add_text_expression(measure, text)


def add_dal_segno(measure, text="D.S. al Fine"):
    """添加 D.S. al Fine 标记。"""
    add_text_expression(measure, text)


def add_fine(measure):
    """添加 Fine 标记。"""
    add_text_expression(measure, "Fine")


def add_new_system(measure):
    """在指定小节处强制换行（新系统），用于区分乐章/段落。"""
    measure.insert(0, layout.SystemLayout(isNew=True))


def add_new_page(measure):
    """在指定小节处强制换页，用于区分大乐章。"""
    measure.insert(0, layout.PageLayout(isNew=True))


def renumber_measures(part):
    """把 Part 中所有 Measure 按顺序重新编号为 1, 2, 3, ..."""
    for i, m in enumerate(part.getElementsByClass(stream.Measure), start=1):
        m.number = i


def group_notes_into_measures(notes, time_sig="4/4", start_number=1):
    """把一维 Note/Rest 列表按拍号切分成多个 Measure。

    Args:
        notes: Note 或 Rest 的列表（每个元素需要有 quarterLength）
        time_sig: 拍号字符串
        start_number: 起始小节编号

    Returns:
        list[Measure]
    """
    from music21 import meter
    ts = meter.TimeSignature(time_sig)
    beats_per_measure = ts.barDuration.quarterLength

    measures = []
    current = stream.Measure(number=start_number)
    current.timeSignature = ts
    current_len = 0.0

    for n in notes:
        ql = n.quarterLength
        # 如果当前小节放不下，先收尾并新建小节
        if current_len + ql > beats_per_measure + 1e-9 and current_len > 0:
            measures.append(current)
            start_number += 1
            current = stream.Measure(number=start_number)
            current.timeSignature = ts
            current_len = 0.0

        current.append(n)
        current_len += ql

    if current_len > 0 or len(measures) == 0:
        measures.append(current)

    return measures
