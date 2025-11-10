from functools import reduce

from rich.table import Table
from rich.console import Console
import copy

from genetic_algorithm.work.class_scheduling.domain import SectionSchedule, Time, Group, Professor

console = Console()


def format_time_no_seconds(time: Time):
    hours = time.hour
    minutes = time.minute

    return f"{hours:02d}:{minutes:02d}"

def display_week_schedule(chromosome: list[SectionSchedule], start_hour: Time, end_hour: Time, course_duration: Time, pause_duration: Time,
                          *, for_group=None, for_professor=None):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
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


            start = format_time_no_seconds(s.time_start)
            end = format_time_no_seconds(s.time_end)

            slot = f'{start}-{end}'
            day = days[s.day]

            if day in schedule and slot in schedule[day]:
                info = f"{s.section.subject.name}\n{s.room.name}\n{s.section.meeting_type.name}"

                if for_group:
                    info += "\n" + s.section.professor.name

                if for_professor:
                    info += "\n"
                    info += "\n".join(g.name for g in s.section.group)

                schedule[day][slot] = info


        # Build the table
        title = f"Schedule for Group {for_group}" if for_group else f"Schedule for Prof. {for_professor}"
        table = Table(title=title, show_lines=True, expand=True, min_width=300)

        table.add_column('Hour', justify='center', max_width=20, no_wrap=False)
        for d in days:
            table.add_column(d, justify='center', max_width=25)

        for slot in hours:
            row = [slot]
            for d in days:
                row.append(schedule[d][slot])
            table.add_row(*row)


        console.print(table)


def interactive_schedule(chromosome: list[SectionSchedule], start_hour, end_hour, course_duration, pause_duration, groups, professors):

    group_names = [g.name for g in groups]
    professor_names = [p.name for p in professors]

    while True:
        console.print('\n[bold]Selectează vizualizare:[/bold]')
        console.print("1. Grupă")
        console.print("2. Profesor")
        console.print("3. Ieșire")

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
            console.print("[bold green]Ieșire din vizualizator...[/bold green]")
            break

        else:
            console.print("[red]Alegere invalidă, reîncearcă.[/red]")

