"""
第7课 多进程：乐团协作
教师配套资源：
  1) music21 小型乐团总谱（小提琴、中提琴、大提琴）导出 MusicXML
  2) multiprocessing Queue 同步演示
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

import os as os_module
import time
from multiprocessing import Process, Queue
from music21 import note, stream, instrument
from _score_utils import make_score, make_part


def build_violin_part():
    part = make_part(name="小提琴", instrument_obj=instrument.Violin())
    for n in ["E5", "F#5", "G5", "A5", "B5", "A5", "G5", "F#5"]:
        part.append(note.Note(n, quarterLength=1))
    return part


def build_viola_part():
    part = make_part(name="中提琴", instrument_obj=instrument.Viola())
    for n in ["C5", "D5", "E5", "C5", "G4", "A4", "B4", "G4"]:
        part.append(note.Note(n, quarterLength=1))
    return part


def build_cello_part():
    part = make_part(name="大提琴", instrument_obj=instrument.Violoncello())
    for n in ["C3", "D3", "E3", "F3", "G3", "F3", "E3", "D3"]:
        part.append(note.Note(n, quarterLength=1))
    return part


def musician(q, name, part_notes):
    """模拟乐手：等待指挥信号后演奏。"""
    signal = q.get()
    print(f"[{os_module.getpid()}] {name} 收到: {signal}", flush=True)
    for n in part_notes:
        print(f"  {name} 演奏 {n}", flush=True)
        time.sleep(0.2)


def multiprocessing_demo():
    """多进程 + Queue 同步演示。"""
    print("\n【multiprocessing 乐团同步演示】")
    q = Queue()
    parts = [
        ("小提琴", ["E5", "F#5", "G5", "A5"]),
        ("大提琴", ["C3", "D3", "E3", "F3"]),
    ]
    procs = [Process(target=musician, args=(q, n, p)) for n, p in parts]
    for p in procs:
        p.start()
    time.sleep(0.5)
    q.put("预备——起！")
    for p in procs:
        p.join()


def main():
    print("第7课 多进程：乐团协作")

    # 1. 导出小型乐团总谱
    score = make_score(title="第7课 多进程：乐团协作")
    score.append(build_violin_part())
    score.append(build_viola_part())
    score.append(build_cello_part())
    score.write("musicxml", fp=os.path.join(OUTPUT_DIR, "lesson07_multiprocessing_orchestra.xml"))
    print("已导出：lesson07_multiprocessing_orchestra.xml")

    # 2. 多进程同步演示
    multiprocessing_demo()


if __name__ == "__main__":
    main()
