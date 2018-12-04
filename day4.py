import re

from collections import defaultdict
from datetime import datetime
from utils import get_input

timestamp_dict = {}
time_asleep_dict = defaultdict(int)
guard_to_minute_dict = defaultdict(list)
minute_to_guard_dict = defaultdict(list)


def day4a(puzzle_input: str) -> int:
    global timestamp_dict, time_asleep_dict, guard_to_minute_dict, minute_to_guard_dict
    for line in puzzle_input.strip().split('\n'):
        m = re.match(r'\[\d+-(\d+-\d+ \d+:\d+)\] (Guard #\d+ begins shift|falls asleep|wakes up)', line)
        d = datetime.strptime('2018-{}'.format(m.group(1)), '%Y-%m-%d %H:%M')
        timestamp_dict[d.timestamp()] = (d, m.group(2))

    timestamps = sorted(timestamp_dict.keys())
    asleep, guard = None, -1
    for timestamp in timestamps:
        d, action = timestamp_dict[timestamp]
        if 'shift' in action:
            guard = int(action.replace('Guard #', '').replace(' begins shift', ''))
        if 'asleep' in action:
            asleep = d
        if 'wakes' in action:
            diff = int(timestamp - asleep.timestamp()) // 60
            time_asleep_dict[guard] += diff
            guard_to_minute_dict[guard] += [(asleep.minute + i) % 60 for i in range(diff)]
            for i in range(diff):
                minute_to_guard_dict[(asleep.minute + i) % 60].append(guard)

    largest = sorted(time_asleep_dict.items(), key=lambda kv: kv[1])[-1][0]
    minute = max(guard_to_minute_dict[largest], key=guard_to_minute_dict[largest].count)
    return largest * minute


def day4b(puzzle_input: str) -> int:
    global minute_to_guard_dict
    most_frequent_guard_by_minute = {minute: (lambda guard: (guard, guards.count(guard)))(max(guards, key=guards.count))
                                     for minute, guards in minute_to_guard_dict.items()}
    minute, guard_info = sorted(most_frequent_guard_by_minute.items(), key=lambda kv: kv[1][1])[-1]
    return minute * guard_info[0]


if __name__ == '__main__':
    day4_input = get_input('day4.txt')
    print(day4a(day4_input))
    print(day4b(day4_input))
