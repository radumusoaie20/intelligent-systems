# Class Scheduling

## Problem formulation

Given `n` classes, `m` rooms, `k` days for scheduling (work days),
`d` time for each class (how many hours it takes), a day of
`d_start` and `d_end`, where `d_start` means the start of the work day,
and `d_end` means the end of it (the time interval in which classes can take
place), we are proposing to solve the problem of scheduling the `n` classes
using the `m` rooms in the span of `k` days, plus a pause duration `p` between
classes

## Consideration

In order to simplify the problem, we have decided the following:

- Professor's name are unique (no repeating names)
- The algorithm takes as input the following:
  - The classes that need to be had, specifying the 
  professor who has to teach, the group or groups that needs to be taught and the meeting type
    (`Lab`, `Course` or `Seminar`)
  - The rooms and their sizes
  - The duration of a class
  - The duration of class pauses
  - The number of teaching days
  - The start and end of each working day
  - All courses have the same length

# Solutions

The solution will be represented as a list of `SectionSchedule`
associated with all the `Section` objects (which represent courses)
and the `Room` used at a given start `Time` and end `Time`

