from functools import reduce

from rich.table import Table
from rich.console import Console
import copy

from genetic_algorithm.work.class_scheduling.domain import SectionSchedule, Time, Group, Professor, MeetingType

console = Console()


def format_time_no_seconds(time: Time):
    hours = time.hour
    minutes = time.minute

    return f"{hours:02d}:{minutes:02d}"

def section_type(meeting_type: MeetingType):
    if meeting_type == MeetingType.LAB:
        return "LABORATOR"

    elif meeting_type == MeetingType.COURSE:
        return "CURS"

    elif meeting_type == MeetingType.SEMINAR:
        return "SEMINAR"

    else:
        return ""

def display_week_schedule(chromosome: list[SectionSchedule], start_hour: Time, end_hour: Time, course_duration: Time, pause_duration: Time,
                          *, for_group=None, for_professor=None, for_room=None):
        days = ["Luni", "Marți", "Miercuri", "Joi", "Vineri"]
        hours = []

        st = copy.copy(start_hour)
        while st + course_duration <= end_hour:
            hours.append(f'{format_time_no_seconds(st)}-{format_time_no_seconds(st + course_duration)}')
            st += course_duration + pause_duration

        schedule = {day: {slot: "" for slot in hours} for day in days}

        for s in chromosome:
            if for_group and not any(g.name == for_group for g in s.section.group):
                continue

            if for_professor and not s.section.professor.name == for_professor:
                continue

            if for_room and not s.room.name == for_room:
                continue


            start = format_time_no_seconds(s.time_start)
            end = format_time_no_seconds(s.time_end)

            slot = f'{start}-{end}'
            day = days[s.day]

            if day in schedule and slot in schedule[day]:
                info = f"{s.section.subject.name}"

                if for_group:
                    info += "\n\n" + s.section.professor.name + "\n" + s.room.name

                if for_professor:
                    info += "\n"
                    info += "\n".join(g.name for g in s.section.group)
                    info += "\n\n" + s.room.name

                if for_room:
                    info += "\n"
                    info += "\n".join(g.name for g in s.section.group)
                    info += "\n\n" + s.section.professor.name

                info += "\n\n" + f"{section_type(s.section.meeting_type)}"
                schedule[day][slot] = info


        # Build the table
        title = f"Orar"
        if for_group:
            title += f" grupa {for_group}"

        elif for_professor:
            title += f" profesor {for_professor}"

        else:
            title += f" sală {for_room}"


        table = Table(title=title, show_lines=True, expand=True, min_width=300)

        table.add_column('Oră', justify='center', max_width=20, no_wrap=False)
        for d in days:
            table.add_column(d, justify='center', max_width=25)

        for slot in hours:
            row = [slot]
            for d in days:
                row.append(schedule[d][slot])
            table.add_row(*row)


        console.print(table)


def interactive_schedule(chromosome: list[SectionSchedule], start_hour, end_hour, course_duration, pause_duration, groups, professors,
                         rooms):

    group_names = [g.name for g in groups]
    professor_names = [p.name for p in professors]

    room_names = [r.name for r in rooms]

    while True:
        console.print('\n[bold]Selectează vizualizare:[/bold]')
        console.print("1. Grupă")
        console.print("2. Profesor")
        console.print("3. Sală")
        console.print("4. Ieșire")

        choice = input("Introdu alegerea ta: ").strip()

        if choice == '1':
            console.print(f"Grupe existente: \n{'\n'.join(group_names)}")
            console.print("\n")
            g = input('Introdu nume grupa: ').strip()
            if g not in group_names:
                console.print(f"[red]Grupa {g} nu a fost găsită![/red].")
                continue
            display_week_schedule(
                chromosome,
                start_hour,
                end_hour,
                course_duration,
                pause_duration,
                for_group=g,
            )

        elif choice == '2':
            console.print(f"Profesori existenți: \n{'\n'.join(professor_names)}")
            p = input('Introdu nume profesor: ').strip()
            if p not in professor_names:
                console.print(f"[red]Profesorul {p} nu a fost găsit![/red].")
                continue

            display_week_schedule(
                chromosome,
                start_hour,
                end_hour,
                course_duration,
                pause_duration,
                for_professor=p
            )
        elif choice == '3':
            console.print(f"Sali existente: \n{'\n'.join(room_names)}")
            p = input("Introdu nume sală:")
            if p not in room_names:
                console.print(f"[red]Sala {p} nu a fost găsită![/red]")

            display_week_schedule(
                chromosome,
                start_hour,
                end_hour,
                course_duration,
                pause_duration,
                for_room=p
            )
        elif choice == '4':
            console.print("[bold green]Ieșire din vizualizator...[/bold green]")
            break

        else:
            console.print("[red]Alegere invalidă, reîncearcă.[/red]")

