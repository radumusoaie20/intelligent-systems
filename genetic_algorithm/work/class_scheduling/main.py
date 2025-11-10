from genetic_algorithm.impl.genetic_algorithm import GeneticAlgorithm
from genetic_algorithm.work.class_scheduling.class_scheduling import (make_section_slots, make_create_individual, select_func, crossover_func,
                                                                      make_mutation, make_fitness_func)
from genetic_algorithm.work.class_scheduling.domain import *
from genetic_algorithm.work.class_scheduling.print_utils import display_week_schedule, interactive_schedule

# Time

t_08_00 = Time(8, 0, 0)
t_09_40 = Time(9, 40, 0)
t_11_20 = Time(11, 20, 0)
t_13_00 = Time(13, 0, 0)
t_14_40 = Time(14, 40, 0)
t_16_20 = Time(16, 20, 0)
t_18_00 = Time(18, 0, 0)
t_19_40 = Time(19, 40, 0)
t_21_10 = Time(21, 10, 0)

day_start = Time(8, 0, 0)
day_end = Time(21, 10, 0)
pause_time = Time(0, 10, 0)

duration = Time(1, 30, 0)

# Specializari

spec_calc = Specialization('Calculatoare')
spec_ti = Specialization('TI')
spec_ism = Specialization('ISM')

specializations = [spec_calc, spec_ti, spec_ism, spec_ism]


# Grupe

g_c_41_1 = Group('C_41/1', spec_calc, 17)
g_c_41_2 = Group('C_41/2', spec_calc, 16)
g_c_42_1 = Group('C_42/1', spec_calc, 13)
g_c_42_2 = Group('C_42/2', spec_calc, 15)
g_c_42_3 = Group('C_42/3', spec_calc, 12)

g_ti_41 = Group('TI_41', spec_ti, 18)

g_ism_41_1 = Group('ISM_41/1', spec_ism, 13)
g_ism_41_2 = Group('ISM_41/2', spec_ism, 11)

groups = [g_c_41_1, g_c_41_2, g_c_42_1, g_c_42_2, g_c_42_3,
          g_ti_41, g_ism_41_1, g_ism_41_2]

# Profesori

prof_arpad = Professor('Gellert Arpad', t_09_40, t_21_10)
prof_morariu = Professor('Morariu Daniel', t_09_40, t_21_10)
prof_vasile = Professor('Craciunean Vasile', t_16_20, t_18_00)
prof_bala = Professor('Zamfirescu Bala', t_18_00, t_21_10)
prof_andrei = Professor('Patrausanu Andrei', t_16_20, t_21_10)
prof_florea = Professor('Florea Adrian', t_08_00, t_21_10)
prof_brad = Professor('Brad Remus', t_09_40, t_19_40)
prof_bratu = Professor('Bratu Marius', t_16_20, t_21_10)
prof_daniel = Professor('Craciunean Daniel', t_14_40, t_21_10)
prof_neghina = Professor('Neghina Mihai', t_08_00, t_21_10)
prof_matei = Professor('Matei Alexandru', t_11_20, t_21_10)
prof_liviu = Professor('Popescu Liviu', t_08_00, t_21_10)
prof_berghia = Professor('Berghia Stefania', t_08_00, t_19_40)
prof_beleiu = Professor('Beleiu Iulia', t_16_20, t_19_40)
prof_zabava = Professor('Zabava Dumitru', t_18_00, t_21_10)
prof_catalina = Professor('Neghina Catalina', t_08_00, t_21_10)
prof_pitic = Professor('Pitic Antoniu', t_08_00, t_21_10)
prof_constantinescu = Professor('Constantinescu Constantin', t_08_00, t_19_40)
prof_barglazan = Professor('Barglazan Adrian', t_18_00, t_21_10)
prof_serbanescu = Professor('Serbanescu Andrei', t_18_00, t_21_10)
prof_cretulescu = Professor('Cretulescu Radu', t_08_00, t_14_40)
prof_breazu =  Professor('Breazu Macarie', t_09_40, t_19_40)

professors = [
    prof_arpad, prof_morariu, prof_vasile, prof_bala,
    prof_andrei, prof_florea, prof_bratu, prof_daniel,
    prof_neghina, prof_matei, prof_liviu,
    prof_beleiu, prof_berghia, prof_zabava, prof_catalina, prof_pitic,
    prof_constantinescu, prof_serbanescu, prof_cretulescu, prof_breazu,
    prof_brad, prof_barglazan
]

# Subiecte

sub_img_proc = Subject('Prelucrarea imaginilor')
sub_ml = Subject('Invatare automata')
sub_android = Subject('Elemente de informatica mobila')
sub_int_sys = Subject('Sisteme inteligente')
sub_soac = Subject('Simularea si optimizarea arhitecturilor de calcul')
sub_cybersec = Subject('Securitatea datelor')
sub_signal = Subject('Procesarea semnalelor')
sub_game_prg = Subject('Programarea jocurilor')
sub_encoding = Subject('Codificarea informatiei multimedia')
sub_discrete_sys = Subject('Sisteme dinamice cu evenimente discrete')

subjects = [
    sub_img_proc, sub_ml, sub_android, sub_int_sys,
    sub_soac, sub_cybersec, sub_signal, sub_game_prg,
    sub_encoding, sub_discrete_sys
]


# Sali

r_im_414 = Room('IM414', 23)
r_ie_305 = Room('IE305', 17)
r_im_201 = Room('IM201', 120)
r_im_216 = Room('IM216', 19)
r_im_405 = Room('IM405', 120)
r_ie_006 = Room('IE006', 30)
r_ie_113 = Room('IE113', 20)
r_im_321 = Room('IM321', 23)
r_ie_002 = Room('IE002', 22)
r_im_219 = Room('IM219', 25)
r_im_323 = Room('IM323', 40)
r_ie_303 = Room('IE303', 40)
r_ie_003 = Room('IE003', 30)
r_ie_304 = Room('IE304', 24)
r_ntt_data = Room('NTTData_Evolution', 27)
r_ie_101 = Room('IE101', 40)
r_im_320 = Room('IM320', 23)

rooms = [
    r_im_414, r_ie_305, r_im_201, r_im_216, r_im_405, r_ie_006, r_ie_113,
    r_im_321, r_ie_002, r_im_219, r_im_323, r_ie_303, r_ie_003,
    r_ie_304, r_ntt_data, r_ie_101, r_im_320
]

# Cursuri

g_c = {g_c_41_1, g_c_41_2, g_c_42_1, g_c_42_2, g_c_42_3}
g_c_ti = {g_c_41_1, g_c_41_2, g_c_42_1, g_c_42_2, g_c_42_3, g_ti_41}

sections = [
    # ISM

    # Courses
    Section(MeetingType.COURSE, sub_game_prg, {g_ism_41_1, g_ism_41_2}, prof_pitic, duration),
    Section(MeetingType.COURSE, sub_ml, {g_ism_41_1, g_ism_41_2}, prof_morariu, duration),
    Section(MeetingType.COURSE, sub_encoding, {g_ism_41_1, g_ism_41_2}, prof_breazu, duration),
    Section(MeetingType.COURSE, sub_signal, {g_ism_41_1, g_ism_41_2}, prof_catalina, duration),
    Section(MeetingType.COURSE, sub_img_proc, {g_ism_41_1, g_ism_41_2}, prof_brad, duration),
    Section(MeetingType.COURSE, sub_discrete_sys, {g_ism_41_1, g_ism_41_2}, prof_cretulescu, duration),
    Section(MeetingType.COURSE, sub_android, {g_ism_41_1, g_ism_41_2}, prof_daniel, duration),
    # Lab
    Section(MeetingType.LAB, sub_game_prg, {g_ism_41_1, g_ism_41_2}, prof_serbanescu, duration),
    Section(MeetingType.LAB, sub_ml, {g_ism_41_1}, prof_constantinescu, duration),
    Section(MeetingType.LAB, sub_ml, {g_ism_41_2}, prof_constantinescu, duration),
    Section(MeetingType.LAB, sub_encoding, {g_ism_41_1}, prof_barglazan, duration),
    Section(MeetingType.LAB, sub_encoding, {g_ism_41_2}, prof_barglazan, duration),
    Section(MeetingType.LAB, sub_signal, {g_ism_41_1}, prof_catalina, duration),
    Section(MeetingType.LAB, sub_signal, {g_ism_41_2}, prof_catalina, duration),
    Section(MeetingType.LAB, sub_img_proc, {g_ism_41_1}, prof_catalina, duration),
    Section(MeetingType.LAB, sub_img_proc, {g_ism_41_2}, prof_catalina, duration),
    Section(MeetingType.LAB, sub_android, {g_ism_41_1}, prof_daniel, duration),
    Section(MeetingType.LAB, sub_android, {g_ism_41_2}, prof_daniel, duration),
    Section(MeetingType.LAB, sub_discrete_sys, {g_ism_41_1}, prof_cretulescu, duration),
    Section(MeetingType.LAB, sub_discrete_sys, {g_ism_41_2}, prof_cretulescu, duration),

    # TI

    # Courses
    Section(MeetingType.COURSE, sub_android, g_c_ti, prof_vasile, duration),
    Section(MeetingType.COURSE, sub_int_sys, g_c_ti, prof_bala, duration),
    Section(MeetingType.COURSE, sub_signal, {g_ti_41}, prof_catalina, duration),
    Section(MeetingType.COURSE, sub_img_proc, {g_ti_41}, prof_brad, duration),
    Section(MeetingType.COURSE, sub_soac, g_c_ti, prof_florea, duration),
    Section(MeetingType.COURSE, sub_cybersec, g_c_ti, prof_brad, duration),
    Section(MeetingType.COURSE, sub_ml, g_c_ti, prof_morariu, duration),
    # Lab
    Section(MeetingType.LAB, sub_android, {g_ti_41}, prof_daniel, duration),
    Section(MeetingType.LAB, sub_int_sys, {g_ti_41}, prof_matei, duration),
    Section(MeetingType.LAB, sub_signal, {g_ti_41}, prof_catalina, duration),
    Section(MeetingType.LAB, sub_img_proc, {g_ti_41}, prof_arpad, duration),
    Section(MeetingType.LAB, sub_soac, {g_ti_41}, prof_andrei, duration),
    Section(MeetingType.LAB, sub_cybersec, {g_ti_41}, prof_liviu, duration),
    Section(MeetingType.LAB, sub_ml, {g_ti_41}, prof_berghia, duration),

    # C

    # Courses
    Section(MeetingType.COURSE, sub_signal, g_c, prof_neghina, duration),
    Section(MeetingType.COURSE, sub_img_proc, g_c, prof_brad, duration),

    # Lab

    Section(MeetingType.LAB, sub_img_proc, {g_c_41_1}, prof_arpad, duration),
    Section(MeetingType.LAB, sub_ml, {g_c_41_1}, prof_morariu, duration),
    Section(MeetingType.LAB, sub_soac, {g_c_41_1}, prof_andrei, duration),
    Section(MeetingType.LAB, sub_cybersec, {g_c_41_1}, prof_bratu, duration),
    Section(MeetingType.LAB, sub_android, {g_c_41_1}, prof_daniel, duration),
    Section(MeetingType.LAB, sub_signal, {g_c_41_1}, prof_neghina, duration),
    Section(MeetingType.LAB, sub_int_sys, {g_c_41_1}, prof_matei, duration),

    Section(MeetingType.LAB, sub_img_proc, {g_c_41_2}, prof_arpad, duration),
    Section(MeetingType.LAB, sub_ml, {g_c_41_2}, prof_morariu, duration),
    Section(MeetingType.LAB, sub_soac, {g_c_41_2}, prof_andrei, duration),
    Section(MeetingType.LAB, sub_cybersec, {g_c_41_2}, prof_bratu, duration),
    Section(MeetingType.LAB, sub_android, {g_c_41_2}, prof_daniel, duration),
    Section(MeetingType.LAB, sub_signal, {g_c_41_2}, prof_neghina, duration),
    Section(MeetingType.LAB, sub_int_sys, {g_c_41_2}, prof_matei, duration),

    Section(MeetingType.LAB, sub_img_proc, {g_c_42_1}, prof_arpad, duration),
    Section(MeetingType.LAB, sub_ml, {g_c_42_1}, prof_berghia, duration),
    Section(MeetingType.LAB, sub_soac, {g_c_42_1}, prof_beleiu, duration),
    Section(MeetingType.LAB, sub_cybersec, {g_c_42_1}, prof_liviu, duration),
    Section(MeetingType.LAB, sub_android, {g_c_42_1}, prof_daniel, duration),
    Section(MeetingType.LAB, sub_signal, {g_c_42_1}, prof_zabava, duration),
    Section(MeetingType.LAB, sub_int_sys, {g_c_42_1}, prof_matei, duration),

    Section(MeetingType.LAB, sub_img_proc, {g_c_42_2}, prof_arpad, duration),
    Section(MeetingType.LAB, sub_ml, {g_c_42_2}, prof_berghia, duration),
    Section(MeetingType.LAB, sub_soac, {g_c_42_2}, prof_beleiu, duration),
    Section(MeetingType.LAB, sub_cybersec, {g_c_42_2}, prof_liviu, duration),
    Section(MeetingType.LAB, sub_android, {g_c_42_2}, prof_daniel, duration),
    Section(MeetingType.LAB, sub_signal, {g_c_42_2}, prof_zabava, duration),
    Section(MeetingType.LAB, sub_int_sys, {g_c_42_2}, prof_matei, duration),

    Section(MeetingType.LAB, sub_img_proc, {g_c_42_3}, prof_arpad, duration),
    Section(MeetingType.LAB, sub_ml, {g_c_42_3}, prof_berghia, duration),
    Section(MeetingType.LAB, sub_soac, {g_c_42_3}, prof_andrei, duration),
    Section(MeetingType.LAB, sub_cybersec, {g_c_42_3}, prof_bratu, duration),
    Section(MeetingType.LAB, sub_android, {g_c_42_3}, prof_daniel, duration),
    Section(MeetingType.LAB, sub_signal, {g_c_42_3}, prof_neghina, duration),
    Section(MeetingType.LAB, sub_int_sys, {g_c_42_3}, prof_matei, duration),
]

# precompute time slots
section_slots = make_section_slots(sections, day_start, day_end, pause_time)

# need a creator for individual chromosomes
create_individual = make_create_individual(sections, section_slots, rooms)

# mutation function
mutation_func = make_mutation(section_slots, rooms)

# fitness function
fitness_func = make_fitness_func(day_start, day_end)

# GA
ga = GeneticAlgorithm(
    population_size=50,
    fitness_func=fitness_func,
    create_individual_func=create_individual,
    selection_func=select_func,
    crossover_func=crossover_func,
    mutation_func=mutation_func,
    crossover_rate=0.7,
    mutation_rate=0.8,
    elitism_count=4,
    explorative_elitism=False,
    minimize_solution=False
)

best, best_f = ga.run(num_generations=100, verbose=True)

print(f"Gasit configuratia cu scor: {best_f}")

# Interactive tabular views
interactive_schedule(best, day_start, day_end, duration, pause_time, groups, professors)