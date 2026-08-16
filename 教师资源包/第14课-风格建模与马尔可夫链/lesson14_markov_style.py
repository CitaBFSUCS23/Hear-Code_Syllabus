"""
第14课 风格建模与马尔可夫链（本科进阶）
教师配套资源：用 music21 corpus 分析巴赫众赞歌，构建一阶马尔可夫链生成旋律
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

import random
from collections import Counter
from music21 import corpus, note, stream
from _score_utils import make_score, make_part


def get_corpus_melody():
    """尝试从 music21 corpus 加载巴赫众赞歌；失败则使用内置备选旋律。"""
    try:
        bwv = corpus.parse("bwv256")
        notes = [n for n in bwv.recurse().notes if isinstance(n, note.Note)]
        print(f"  成功加载 corpus 'bwv256'，共 {len(notes)} 个音符")
        return notes
    except Exception as e:
        print(f"  corpus 加载失败（{e}），使用备选旋律")
        fallback_pitches = [60, 62, 64, 65, 64, 62, 60, 59, 60, 62, 64, 65,
                            67, 65, 64, 62, 60, 59, 57, 60]
        return [note.Note(midi=p, quarterLength=1) for p in fallback_pitches]


def build_markov_chain(notes):
    """构建一阶马尔可夫链：{midi: [interval1, interval2, ...]}。"""
    transitions = {}
    for i in range(len(notes) - 1):
        current = notes[i].pitch.midi
        nxt = notes[i + 1].pitch.midi
        interval = nxt - current
        transitions.setdefault(current, []).append(interval)
    return transitions


def generate_melody(transitions, start_midi=60, length=16, seed=42):
    """根据马尔可夫链生成新旋律。"""
    random.seed(seed)
    current = start_midi
    melody = [note.Note(midi=current, quarterLength=1)]
    for _ in range(length - 1):
        if current in transitions and transitions[current]:
            interval = random.choice(transitions[current])
            current += interval
            # 限制在合理音域
            current = max(48, min(79, current))
        melody.append(note.Note(midi=current, quarterLength=1))
    return melody


def main():
    print("第14课 风格建模与马尔可夫链")

    source_notes = get_corpus_melody()

    # 1. 统计最常见音程
    intervals = []
    for i in range(len(source_notes) - 1):
        intervals.append(source_notes[i + 1].pitch.midi - source_notes[i].pitch.midi)
    counter = Counter(intervals)
    print("\n【最常见音程 TOP5】")
    for interval, count in counter.most_common(5):
        direction = "上行" if interval > 0 else "下行" if interval < 0 else "同音"
        print(f"  音程 {interval:+d} 半音 ({direction}): {count} 次")

    # 2. 构建一阶马尔可夫链
    transitions = build_markov_chain(source_notes)
    print(f"\n  马尔可夫链状态数：{len(transitions)}")

    # 3. 生成新旋律并导出
    generated = generate_melody(transitions, start_midi=60, length=16, seed=42)
    melody_part = make_part(name="马尔可夫生成旋律")
    for n in generated:
        melody_part.append(n)

    score = make_score(title="第14课 马尔可夫链生成旋律")
    score.append(melody_part)
    score.write("musicxml", fp=os.path.join(OUTPUT_DIR, "lesson14_markov_generated.xml"))
    print("\n已导出：lesson14_markov_generated.xml （一阶马尔可夫链生成）")


if __name__ == "__main__":
    main()
