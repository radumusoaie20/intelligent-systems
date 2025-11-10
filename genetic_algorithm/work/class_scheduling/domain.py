from enum import Enum
from random import random
from typing import List


class Time:
    def __init__(self, hour, minute, second):
        self.hour = hour
        self.minute = minute
        self.second = second

    def __copy__(self):
        return Time(self.hour, self.minute, self.second)

    def to_seconds(self):
        return (self.hour * 3600) + (self.minute * 60) + self.second

    def __eq__(self, other):
        return self.hour == other.hour and self.minute == other.minute and self.second == other.second

    def __lt__(self, other):
        this_seconds = self.to_seconds()
        other_seconds = other.to_seconds()
        return this_seconds < other_seconds

    def __gt__(self, other):
        this_seconds = self.to_seconds()
        other_seconds = other.to_seconds()
        return this_seconds > other_seconds

    def __le__(self, other):
        this_seconds = self.to_seconds()
        other_seconds = other.to_seconds()
        return this_seconds <= other_seconds

    def __ge__(self, other):
        this_seconds = self.to_seconds()
        other_seconds = other.to_seconds()
        return this_seconds >= other_seconds

    def __int__(self):
        """
        :return: The seconds for this `Time` object
        """
        return self.hour * 60 * 60 + self.minute * 60 + self.second

    def __add__(self, other):
        """
        Adds this `Time` object to `other`
        :param other: The other `Time` object
        :return: A `Time` object representing the sum of this `Time` object and `other`, wrapping around a day (24 hours)
        """
        total_seconds = int(self) + int(other)
        day_seconds = 24 * 60 * 60
        return time_from_seconds(total_seconds % day_seconds)

    def __sub__(self, other):
        """
        Adds this `Time` object to `other`
        :param other: The other `Time` object
        :return: A `Time` object representing the difference of this `Time` object and `other`, wrapping around a day (24 hours)
        """
        total_seconds = int(self) - int(other)
        day_seconds = 24 * 60 * 60
        return time_from_seconds(total_seconds % day_seconds)

    def __str__(self):
        hour = "0" + str(self.hour) if len(str(self.hour)) == 1 else self.hour
        minute = "0" + str(self.minute) if len(str(self.minute)) == 1 else self.minute
        second = "0" + str(self.second) if len(str(self.second)) == 1 else self.second
        return f'{hour}:{minute}:{second}'

    def __hash__(self):
        return self.to_seconds()


def time_from_seconds(seconds: int):
    hour = seconds // 3600
    minute = seconds % 3600 // 60
    second = seconds % 60
    return Time(hour, minute, second)

def time_from_start_and_duration(start: Time, duration_in_minutes: int) -> (Time, Time):
    return start, time_from_seconds(int(start) + duration_in_minutes * 60)  # returns in seconds


class Professor:
    def __init__(self, name: str, start_hour: Time, end_hour: Time):
        """
        Constructs a professor. For example
        :param name: The name of the professor
        :param start_hour: The start hour of the professor (when he can teach)
        :param end_hour: The end hour of the professor (when he has to leave and cannot teach)
        """
        self.name = name
        self.start_hour = start_hour
        self.end_hour = end_hour

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


class Specialization:
    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


class Room:
    def __init__(self, name: str, max_size: int):
        self.name = name
        self.max_size = max_size

    def __eq__(self, other):
        return self.name == other.name and self.max_size == other.max_size

    def __hash__(self):
        return hash(self.name) + 11 * self.max_size

class Group:
    def __init__(self, name: str, specialization: Specialization, size: int):
        self.specialization = specialization
        self.name = name
        self.size = size

    def __eq__(self, other):
        return self.specialization == other.specialization and self.name == other.name

    def __hash__(self):
        return hash(self.name) + 31 * self.size + hash(self.specialization) * 13

class MeetingType(Enum):
    COURSE = 1
    LAB = 2
    SEMINAR = 3

class Subject:
    def __init__(self, name: str):
        """
        Constructs a subject.
        :param name: The name of the subject
        """
        self.name = name

    def __eq__(self, other):
        return  self.name == other.name or self.name in other.__other_names

    def __hash__(self):
        return hash(self.name)

class Section:
    def __init__(self, meeting_type: MeetingType, subject: Subject, group: set[Group], professor: Professor,
                 duration: Time):
        """
        Constructs a section.
        :param meeting_type: The type of meeting (laboratory, course or seminar)
        :param subject: The subject of the meeting
        :param group: The group(s) that is having the meeting
        :param professor: The professor assigned to hold the meeting
        :param duration: The duration of the meeting
        """
        self.meeting_type = meeting_type
        self.subject = subject
        self.group = group
        self.professor = professor
        self.duration = duration

    def __eq__(self, other):
        return self.meeting_type == other.meeting_type and self.subject == other.subject and self.group == other.group and self.professor == other.professor and self.duration == other.duration

    def __hash__(self):
        return hash(self.meeting_type) * 13 + hash(frozenset(self.group)) * 31 + hash(self.professor) * 17 + hash(self.duration) * 23 + hash(self.subject) * 17

class SectionSchedule:
    def __init__(self, section: Section, room: Room, time_start: Time, day: int):
        """
        Constructs a section schedule.
        :param section: The section for which the schedule will be created
        :param time_start: The start time of the section
        :param room: The room of the section
        :param day: The day of the week
        """

        self.students_size = sum(g.size for g in section.group)
        self.section = section
        self.time_start = time_start
        self.time_end = time_start + section.duration
        self.room = room
        self.day = day

    def exceeds_room_size(self) -> bool:
        """
        Checks if the number of students exceeds the room size.
        :return: `True` if the number of students exceeds the room size, `False` otherwise
        """
        return self.students_size > self.room.max_size

    def is_outside_of_professor_time(self) -> bool:
        """
        Checks if the section is outside the professor time.
        :return: `True` if the section is outside the professor time, `False` otherwise
        """
        prof = self.section.professor
        return not (self.time_start >= prof.start_hour and self.time_end <= prof.end_hour)

    def is_before(self, other):
        """
        :param other: The other `SectionSchedule`
        :return: `True` if the section is before the other `SectionSchedule`
        """
        return self.time_end + self.day * 24 * 60 * 60 < other.time_start + other.day * 24 * 60 * 60

    def is_after(self, other):
        """
       :param other: The other `SectionSchedule`
       :return: `True` if the section is after the other `SectionSchedule`
       """
        return self.time_start + self.day * 24 * 60 * 60 > other.time_end + other.day * 24 * 60 * 60

    def __eq__(self, other):
        return (self.section == other.section and self.time_start == other.time_start and self.time_end == other.time_end
                    and self.room == other.room and self.day == other.day)

    def __str__(self):
        return (f"Subject: {self.section.subject.name} \n"
                f"Professor: {self.section.professor.name} \n"
                f"Room: {self.room.name}, Size: {self.room.max_size} \n"
                f"Number of students: {self.students_size} \n"
                f"Day: {self.day} \n"
                f"{str(self.time_start)} - {self.time_end} \n")

    def __hash__(self):
        return self.time_start.__hash__() * 17 + self.section.__hash__() * 13 + self.room.__hash__() * 31 + self.day * 23

class ClassScheduling:

    def __init__(self, class_duration: int, pause_duration: int,
                teaching_days: int, sections: List[Section], day_time_start: Time, day_time_end: Time):
        self.class_duration = class_duration
        self.pause_duration = pause_duration
        self.teaching_days = teaching_days
        self.sections = sections
        self.day_time_start = day_time_start
        self.day_time_end = day_time_end
