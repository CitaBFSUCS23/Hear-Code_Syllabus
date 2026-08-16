"""
第6课 多线程：钢琴左右手
教师配套资源：
  1) music21 静态多声部钢琴 Score（导出 MusicXML）
  2) threading 运行时并发演示（终端打印）
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

import threading
import time
from music21 import note, stream, instrument
from _score_utils import make_score, make_part


def build_right_hand():
    """右手旋律。"""
    part = make_part(name="右手", instrument_obj=instrument.Piano())
    for n in ["C5", "E5", "G5", "E5", "D5", "F5", "A5", "G5"]:
        part.append(note.Note(n, quarterLength=1))
    return part


def build_left_hand():
    """左手分解和弦伴奏。"""
    part = make_part(name="左手", instrument_obj=instrument.Piano())
    for n in ["C3", "G3", "E3", "G3", "F3", "C3", "G3", "C3"]:
        part.append(note.Note(n, quarterLength=1))
    return part


def threading_demo():
    """用 threading 模拟左右手同时演奏，演示共享变量与锁。"""
    beat = 0
    lock = threading.Lock()

    def play_hand(name, notes):
        nonlocal beat
        for n in notes:
            with lock:
                beat += 1
                print(f"{name}: {n} (第{beat}拍)", flush=True)
            time.sleep(0.3)

    print("\n【threading 并发演示】")
    right_notes = ["C5", "E5", "G5"]
    left_notes = ["C3", "G3", "E3"]
    t1 = threading.Thread(target=play_hand, args=("右手", right_notes))
    t2 = threading.Thread(target=play_hand, args=("左手", left_notes))
    t1.start()
    t2.start()
    t1.join()
    t2.join()


def main():
    print("第6课 多线程：钢琴左右手")

    # 1. 导出多声部钢琴乐谱
    score = make_score(title="第6课 多线程：钢琴左右手")
    score.append(build_right_hand())
    score.append(build_left_hand())
    score.write("musicxml", fp=os.path.join(OUTPUT_DIR, "lesson06_threading_piano.xml"))
    print("已导出：lesson06_threading_piano.xml")

    # 2. 演示运行时并发
    threading_demo()


if __name__ == "__main__":
    main()
