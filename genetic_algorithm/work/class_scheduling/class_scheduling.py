from random import choice, sample, randint
from copy import copy

from genetic_algorithm.work.class_scheduling.domain import *

# Chromosome length will be determined by the number of classes that need to be scheduled (each class needed to be taught represents one gene)

# Utility

def section_time_slots(section: Section, start: Time, end: Time, pause_time: Time) -> list[(Time, Time)]:

    result: list[(Time, Time)] = []

    # We will limit the `start` and `end` to the professors available time
    start = max(start, section.professor.start_hour) # Profs mostly start later (a bigger time value)
    end = min(end, section.professor.end_hour) # Profs cannot teach after their work day is over (which is less than the end time)

    current_state = copy(start)

    while current_state + section.duration <= end:
        result.append((copy(current_state), current_state + section.duration))
        current_state = current_state + section.duration + pause_time

    return result

def make_section_slots(sections, day_start, day_end, pause_time):
    section_slots = {}
    for sec in sections:
        # limit day window to professor availability
        prof_start = max(day_start, sec.professor.start_hour)
        prof_end = min(day_end, sec.professor.end_hour)
        # generate slots for that section's duration (returns list of (start, end) Time)
        slots = section_time_slots(sec, prof_start, prof_end, pause_time)
        if not slots:
            raise ValueError(f"No valid slots for section {sec} given professor/working hours")
        section_slots[sec] = slots
    return section_slots


# We will take the approach of generating valid scheduling objects (meaning that it respects the prof schedule and the room size)
# The fitness function will hard penalize all the resulting individuals (`SectionSchedule`) in case they
# have overlapping rooms or professors or groups
# We need a function with no params, so we need to use a wrapper to get the method

def make_create_individual(sections, section_slots, rooms):
    def create_individual_solution():
        chromosome = []
        for section in sections:

            if not len(section_slots[section]):
                raise Exception('No time available to take the section {} with the prof'.format(section, section.professor))

            start, _ = choice(section_slots[section])  # Pick a random time slot for the section

            possible_rooms = [r for r in rooms if r.max_size >= sum(g.size for g in section.group)]

            if not len(possible_rooms):
                raise Exception('No rooms available for section {}'.format(section))

            day = randint(0, 4)

            room = choice(possible_rooms)  # pick a random room from the possible rooms
            chromosome.append(SectionSchedule(section, room, start, day))

        return chromosome

    return create_individual_solution


# Parent selection (random selection)
def select_func(population: list[list[SectionSchedule]], fitness_scores: list[float]):
    parent1, parent2 =  sample(population, k=2)
    return parent1, parent2

# Cross-over
# A solution is basically a list of schedules for sections (the order is maintained because sections is a list)
# We will do a single point crossover
def crossover_func(parent1: list[SectionSchedule], parent2: list[SectionSchedule]):

    size = len(parent1)
    point = randint(1, size - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]

    return child1, child2


# Mutation

def make_mutation(section_slots, rooms):
    def mutation_func(chromosome: list[SectionSchedule]):
        for i, gene in enumerate(chromosome):

            # pick time slot that fits professor day
            start, end = choice(section_slots[gene.section])

            # pick valid room
            possible_rooms = [r for r in rooms if r.max_size >= sum(g.size for g in gene.section.group)]
            room = choice(possible_rooms)

            # pick another day maybe?
            day = randint(0, 4)

            chromosome[i] = SectionSchedule(gene.section, room, start, day)

            return chromosome

    return mutation_func

# Fitness evaluation
# As a note, our solution doesn't filter out impossible solutions (like a professor having 2 courses at the same time)
# We are relying on the fact that since these solutions tend to bring a big penalty, they will cease to propagate throughout generations
# leading to their disappearance
# So this means that we are taking a risk in case the initial population tends to spawn invalid solutions

def make_fitness_func(day_start: Time, day_end: Time):
    def fitness_func(chromosome: list[SectionSchedule]) -> float:
        penalty = 0

        # Check overlaps for the chromosome (solution) schedules (for each pair)
        # Kind of like doing bubble sort

        # Hard constraints mostly (big penalty yields in almost 0 chance of selecting it as a viable solution)
        for i, a in enumerate(chromosome):
            for j, b in enumerate(chromosome):
                if i >= j: continue # mimics bubble sort, finding pairs

                # Room conflict (both sections take place in the same room at approximately the same time)
                if a.room == b.room and not (a.is_before(b) or a.is_after(b)):
                    penalty += 1000

                # Professor conflict (the sections are being taught by the same professor at approximately the same time)
                if a.section.professor == b.section.professor and not (a.is_before(b) or a.is_after(b)):
                    penalty += 1000

                # Group conflict (a group takes two sections at the same time)
                if not a.section.group.isdisjoint(b.section.group) and not (a.is_before(b) or a.is_after(b)):
                    penalty += 1000

        # Soft constraints (Help with optimization)

        # Minimize professor gaps
        penalty += professor_idle_penalty(chromosome, day_start, day_end) * 9

        # Minimize groups gaps
        penalty += group_idle_penalty(chromosome, day_start, day_end) * 4

        # Penalize placing a small number of students in big rooms
        penalty += room_size_penalty(chromosome) * 2

        return 1 / (1 + penalty) # when penalty is high, the value is low, so that means higher fitness means worse solution (maximizing)

    return fitness_func

def professor_idle_penalty(chromosome: list[SectionSchedule], day_start: Time, day_end: Time) -> float:
    penalty = 0

    # Given the solution, we have to find out for the professor his schedule
    prof_sections = {}
    for schedule in chromosome:
        prof = schedule.section.professor
        prof_sections.setdefault(prof, []).append(schedule)


    for prof, sections in prof_sections.items():

        # Grouping by day
        sections_by_day = {}
        for section in sections:
            sections_by_day.setdefault(section.day, []).append(section)

        for day, day_sections in sections_by_day.items():

           # Gap before first class
           first = day_sections[0]
           penalty += int(first.time_start - first.section.professor.start_hour)

           # Gap between consecutives classes
           day_sections.sort(key=lambda s: int(s.time_start)) # sorting within the day

           for i in range(len(day_sections) - 1):
            current_end = int(day_sections[i].time_end)
            next_start = int(day_sections[i + 1].time_start)

            gap_minutes = (next_start - current_end) // 60

            penalty += gap_minutes

            # Gap between last class and end
            last = day_sections[-1]
            penalty += int(last.section.professor.end_hour - last.time_end)

    return penalty

def group_idle_penalty(chromosome: list[SectionSchedule], day_start: Time, day_end: Time) -> float:

    penalty = 0

    group_sections = {}
    for schedule in chromosome:
        for g in schedule.section.group:
            group_sections.setdefault(g, []).append(schedule)


    for g, sections in group_sections.items():

        # Group by day
        sections_by_day = {}
        for section in sections:
            sections_by_day.setdefault(section.day, []).append(section)

        for day, day_sections in sections_by_day.items():

            # Gap before first class
            first = day_sections[0]
            penalty += int(first.time_start - day_start)

            day_sections.sort(key=lambda s: int(s.time_start))

            for i in range(len(day_sections) - 1):
                current_end = int(day_sections[i].time_end)
                next_start = int(sections[i + 1].time_start)
                gap_minutes = (next_start - current_end) // 60

                penalty += gap_minutes

            # Gap between last class and end
            last = day_sections[-1]
            penalty += int(day_end - last.time_end)

    return penalty


def room_size_penalty(chromosome: list[SectionSchedule]) -> float:
    penalty = 0

    for schedule in chromosome:
        penalty += schedule.room.max_size - schedule.students_size # rooms are validated at runtime

    return penalty