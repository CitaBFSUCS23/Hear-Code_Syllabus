"""
第15课 音色与配器（本科进阶）
教师配套资源：面向对象封装 Song 类，体验不同乐器音色
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

from music21 import note, stream, instrument, tempo, dynamics, key, chord as chord_module
from _score_utils import make_score, make_part


class Song:
    """封装一首乐曲的标题、速度、声部列表与播放/导出方法。"""

    def __init__(self, title, tempo=120, key_signature=None):
        self.title = title
        self.tempo = tempo
        self.key_signature = key_signature
        self.parts = []

    def add_part(self, part):
        self.parts.append(part)

    def to_score(self):
        score = make_score(title=self.title)
        score.insert(0, tempo.MetronomeMark(number=self.tempo))
        if self.key_signature:
            score.insert(0, self.key_signature)
        for part in self.parts:
            score.append(part)
        return score

    def export_xml(self, filename):
        self.to_score().write("musicxml", fp=os.path.join(OUTPUT_DIR, filename))
        print(f"  已导出：{filename}")


class MelodyGenerator:
    """封装旋律生成参数。"""

    def __init__(self, scale_pitches, rhythm_pattern):
        self.scale_pitches = scale_pitches
        self.rhythm_pattern = rhythm_pattern

    def generate(self, length=8):
        part = make_part(name="生成旋律")
        for i in range(length):
            pitch = self.scale_pitches[i % len(self.scale_pitches)]
            dur = self.rhythm_pattern[i % len(self.rhythm_pattern)]
            part.append(note.Note(pitch, quarterLength=dur))
        return part


def main():
    print("第15课 音色与配器")

    # 创建作品
    song = Song(title="第15课 夏日小品", tempo=108, key_signature=key.Key("C"))

    # 1. 长笛主旋律
    flute_part = make_part(name="长笛", instrument_obj=instrument.Flute())
    flute_part.insert(0, dynamics.Dynamic("mf"))
    melody = ["C5", "D5", "E5", "G5", "E5", "D5", "C5", "G4",
              "A4", "C5", "A4", "G4", "F4", "E4", "D4", "C4"]
    for p in melody:
        flute_part.append(note.Note(p, quarterLength=1))
    song.add_part(flute_part)

    # 2. 大提琴低音
    cello_part = make_part(name="大提琴", instrument_obj=instrument.Violoncello())
    cello_part.insert(0, dynamics.Dynamic("mp"))
    bass = ["C3", "C3", "G2", "G2", "A2", "A2", "F2", "F2",
            "C3", "C3", "G2", "G2", "C3", "G2", "C3", None]
    for p in bass:
        if p is None:
            cello_part.append(note.Rest(quarterLength=1))
        else:
            cello_part.append(note.Note(p, quarterLength=1))
    song.add_part(cello_part)

    # 3. 钢琴和声
    piano_part = make_part(name="钢琴", instrument_obj=instrument.Piano())
    piano_part.insert(0, dynamics.Dynamic("p"))
    chords = [
        ("C3", "E3", "G3"),
        ("C3", "E3", "G3"),
        ("G2", "B2", "D3"),
        ("G2", "B2", "D3"),
        ("F2", "A2", "C3"),
        ("F2", "A2", "C3"),
        ("C3", "E3", "G3"),
        ("C3", "E3", "G3"),
        ("C3", "E3", "G3"),
        ("C3", "E3", "G3"),
        ("G2", "B2", "D3"),
        ("G2", "B2", "D3"),
        ("C3", "E3", "G3"),
        ("G2", "B2", "D3"),
        ("C3", "E3", "G3"),
        ("C3", "E3", "G3"),
    ]
    for grp in chords:
        piano_part.append(chord_module.Chord(grp, quarterLength=1))
    song.add_part(piano_part)

    song.export_xml("lesson15_orchestration_oop.xml")
    print(f"\n作品标题：{song.title}，速度：{song.tempo} BPM，声部数：{len(song.parts)}")

    # 4. 演示 MelodyGenerator 类
    gen = MelodyGenerator(scale_pitches=["C4", "D4", "E4", "G4", "A4"],
                          rhythm_pattern=[1, 0.5, 0.5, 1])
    generated = gen.generate(length=12)
    generated.insert(0, instrument.Violin())

    score_gen = make_score(title="第15课 MelodyGenerator 示例")
    score_gen.append(generated)
    score_gen.write("musicxml", fp=os.path.join(OUTPUT_DIR, "lesson15_melody_generator.xml"))
    print("已导出：lesson15_melody_generator.xml")


if __name__ == "__main__":
    main()
