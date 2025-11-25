from genetic_algorithm.impl.genetic_algorithm import GeneticAlgorithm
from genetic_algorithm.work.class_scheduling.class_scheduling import (make_section_slots, make_create_individual, select_func, crossover_func,
                                                                      make_mutation, make_fitness_func)
from genetic_algorithm.work.class_scheduling.domain import *
from genetic_algorithm.work.class_scheduling.print_utils import interactive_schedule

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

spec_calc = Specialization('Computer Engineering')
spec_ti = Specialization('Information Technology')
spec_ism = Specialization('Multimedia System Engineering')

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

prof_ga = Professor('GA', t_09_40, t_21_10)
prof_md = Professor('MD', t_09_40, t_21_10)
prof_cv = Professor('CV', t_16_20, t_18_00)
prof_zb = Professor('ZB', t_18_00, t_21_10)
prof_pa = Professor('PA', t_16_20, t_21_10)
prof_fa = Professor('FA', t_08_00, t_21_10)
prof_br = Professor('BR', t_09_40, t_19_40)
prof_bm = Professor('BM', t_16_20, t_21_10)
prof_cd = Professor('CD', t_14_40, t_21_10)
prof_nm = Professor('NM', t_08_00, t_21_10)
prof_ma = Professor('MA', t_11_20, t_21_10)
prof_pv = Professor('PV', t_08_00, t_21_10)
prof_bs = Professor('BS', t_08_00, t_19_40)
prof_bi = Professor('BI', t_16_20, t_19_40)
prof_zd = Professor('ZD', t_18_00, t_21_10)
prof_nc = Professor('NC', t_08_00, t_21_10)
prof_pi = Professor('PI', t_08_00, t_21_10)
prof_cc = Professor('CC', t_08_00, t_19_40)
prof_ba = Professor('BA', t_18_00, t_21_10)
prof_sa = Professor('SA', t_18_00, t_21_10)
prof_cr = Professor('CR', t_08_00, t_14_40)
prof_bre =  Professor('BRE', t_09_40, t_19_40)

professors = [
    prof_ga, prof_md, prof_cv, prof_zb,
    prof_pa, prof_fa, prof_br, prof_cd,
    prof_nm, prof_ma, prof_pv,
    prof_bi, prof_bs, prof_zd, prof_nc, prof_pi,
    prof_cc, prof_sa, prof_cr, prof_bre,
    prof_bm, prof_ba
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
    Section(MeetingType.COURSE, sub_game_prg, {g_ism_41_1, g_ism_41_2}, prof_pi, duration),
    Section(MeetingType.COURSE, sub_ml, {g_ism_41_1, g_ism_41_2}, prof_ma, duration),
    Section(MeetingType.COURSE, sub_encoding, {g_ism_41_1, g_ism_41_2}, prof_bre, duration),
    Section(MeetingType.COURSE, sub_signal, {g_ism_41_1, g_ism_41_2}, prof_nc, duration),
    Section(MeetingType.COURSE, sub_img_proc, {g_ism_41_1, g_ism_41_2}, prof_br, duration),
    Section(MeetingType.COURSE, sub_discrete_sys, {g_ism_41_1, g_ism_41_2}, prof_cr, duration),
    Section(MeetingType.COURSE, sub_android, {g_ism_41_1, g_ism_41_2}, prof_md, duration),
    # Lab
    Section(MeetingType.LAB, sub_game_prg, {g_ism_41_1, g_ism_41_2}, prof_sa, duration),
    Section(MeetingType.LAB, sub_ml, {g_ism_41_1}, prof_cc, duration),
    Section(MeetingType.LAB, sub_ml, {g_ism_41_2}, prof_cc, duration),
    Section(MeetingType.LAB, sub_encoding, {g_ism_41_1}, prof_ba, duration),
    Section(MeetingType.LAB, sub_encoding, {g_ism_41_2}, prof_ba, duration),
    Section(MeetingType.LAB, sub_signal, {g_ism_41_1}, prof_nc, duration),
    Section(MeetingType.LAB, sub_signal, {g_ism_41_2}, prof_nc, duration),
    Section(MeetingType.LAB, sub_img_proc, {g_ism_41_1}, prof_nc, duration),
    Section(MeetingType.LAB, sub_img_proc, {g_ism_41_2}, prof_nc, duration),
    Section(MeetingType.LAB, sub_android, {g_ism_41_1}, prof_md, duration),
    Section(MeetingType.LAB, sub_android, {g_ism_41_2}, prof_md, duration),
    Section(MeetingType.LAB, sub_discrete_sys, {g_ism_41_1}, prof_cr, duration),
    Section(MeetingType.LAB, sub_discrete_sys, {g_ism_41_2}, prof_cr, duration),

    # TI

    # Courses
    Section(MeetingType.COURSE, sub_android, g_c_ti, prof_cv, duration),
    Section(MeetingType.COURSE, sub_int_sys, g_c_ti, prof_zb, duration),
    Section(MeetingType.COURSE, sub_signal, {g_ti_41}, prof_nc, duration),
    Section(MeetingType.COURSE, sub_img_proc, {g_ti_41}, prof_br, duration),
    Section(MeetingType.COURSE, sub_soac, g_c_ti, prof_fa, duration),
    Section(MeetingType.COURSE, sub_cybersec, g_c_ti, prof_br, duration),
    Section(MeetingType.COURSE, sub_ml, g_c_ti, prof_md, duration),
    # Lab
    Section(MeetingType.LAB, sub_android, {g_ti_41}, prof_md, duration),
    Section(MeetingType.LAB, sub_int_sys, {g_ti_41}, prof_ma, duration),
    Section(MeetingType.LAB, sub_signal, {g_ti_41}, prof_nc, duration),
    Section(MeetingType.LAB, sub_img_proc, {g_ti_41}, prof_ga, duration),
    Section(MeetingType.LAB, sub_soac, {g_ti_41}, prof_pa, duration),
    Section(MeetingType.LAB, sub_cybersec, {g_ti_41}, prof_pv, duration),
    Section(MeetingType.LAB, sub_ml, {g_ti_41}, prof_bs, duration),

    # C

    # Courses
    Section(MeetingType.COURSE, sub_signal, g_c, prof_nm, duration),
    Section(MeetingType.COURSE, sub_img_proc, g_c, prof_br, duration),

    # Lab

    Section(MeetingType.LAB, sub_img_proc, {g_c_41_1}, prof_ga, duration),
    Section(MeetingType.LAB, sub_ml, {g_c_41_1}, prof_md, duration),
    Section(MeetingType.LAB, sub_soac, {g_c_41_1}, prof_nc, duration),
    Section(MeetingType.LAB, sub_cybersec, {g_c_41_1}, prof_br, duration),
    Section(MeetingType.LAB, sub_android, {g_c_41_1}, prof_md, duration),
    Section(MeetingType.LAB, sub_signal, {g_c_41_1}, prof_nm, duration),
    Section(MeetingType.LAB, sub_int_sys, {g_c_41_1}, prof_ma, duration),

    Section(MeetingType.LAB, sub_img_proc, {g_c_41_2}, prof_ga, duration),
    Section(MeetingType.LAB, sub_ml, {g_c_41_2}, prof_md, duration),
    Section(MeetingType.LAB, sub_soac, {g_c_41_2}, prof_pa, duration),
    Section(MeetingType.LAB, sub_cybersec, {g_c_41_2}, prof_bm, duration),
    Section(MeetingType.LAB, sub_android, {g_c_41_2}, prof_md, duration),
    Section(MeetingType.LAB, sub_signal, {g_c_41_2}, prof_nm, duration),
    Section(MeetingType.LAB, sub_int_sys, {g_c_41_2}, prof_ma, duration),

    Section(MeetingType.LAB, sub_img_proc, {g_c_42_1}, prof_ga, duration),
    Section(MeetingType.LAB, sub_ml, {g_c_42_1}, prof_bs, duration),
    Section(MeetingType.LAB, sub_soac, {g_c_42_1}, prof_bi, duration),
    Section(MeetingType.LAB, sub_cybersec, {g_c_42_1}, prof_pv, duration),
    Section(MeetingType.LAB, sub_android, {g_c_42_1}, prof_md, duration),
    Section(MeetingType.LAB, sub_signal, {g_c_42_1}, prof_zb, duration),
    Section(MeetingType.LAB, sub_int_sys, {g_c_42_1}, prof_ma, duration),

    Section(MeetingType.LAB, sub_img_proc, {g_c_42_2}, prof_ga, duration),
    Section(MeetingType.LAB, sub_ml, {g_c_42_2}, prof_bs, duration),
    Section(MeetingType.LAB, sub_soac, {g_c_42_2}, prof_bi, duration),
    Section(MeetingType.LAB, sub_cybersec, {g_c_42_2}, prof_pv, duration),
    Section(MeetingType.LAB, sub_android, {g_c_42_2}, prof_md, duration),
    Section(MeetingType.LAB, sub_signal, {g_c_42_2}, prof_zb, duration),
    Section(MeetingType.LAB, sub_int_sys, {g_c_42_2}, prof_ma, duration),

    Section(MeetingType.LAB, sub_img_proc, {g_c_42_3}, prof_ga, duration),
    Section(MeetingType.LAB, sub_ml, {g_c_42_3}, prof_bs, duration),
    Section(MeetingType.LAB, sub_soac, {g_c_42_3}, prof_pa, duration),
    Section(MeetingType.LAB, sub_cybersec, {g_c_42_3}, prof_bm, duration),
    Section(MeetingType.LAB, sub_android, {g_c_42_3}, prof_cd, duration),
    Section(MeetingType.LAB, sub_signal, {g_c_42_3}, prof_nm, duration),
    Section(MeetingType.LAB, sub_int_sys, {g_c_42_3}, prof_ma, duration),
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
    crossover_rate=0.85,
    mutation_rate=0.1,
    elitism_count=4,
    minimize_solution=False
)

best, best_f = ga.run(num_generations=50, verbose=True)

print(f"Gasit configuratia cu scor: {best_f}")

# Interactive tabular views
interactive_schedule(best, day_start, day_end, duration, pause_time, groups, professors, rooms)