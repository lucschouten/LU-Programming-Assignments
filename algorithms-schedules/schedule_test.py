import numpy as np
import typing
import unittest

from schedule import Schedule


class ScheduleFactory(object):

    @staticmethod
    def get_one_day_schedule() -> typing.Tuple[Schedule, typing.List[int]]:
        courses = {
            'A': [0, 1],
            'B': [0],
            'C': [1]
        }
        schedule = Schedule(n_weekdays=1, n_slots_day=5, n_tracks=2,
                            n_rooms=2, courses=courses)
        schedule.schedule[0, 0, 0] = 'B'
        schedule.schedule[0, 0, 1] = 'C'
        schedule.schedule[0, 1, 0] = 'A'
        return schedule, [2, 2, 0]

    @staticmethod
    def get_one_day_schedule_duplicates() -> Schedule:
        courses = {
            'A': [0, 1],
            'B': [0, 1],
            'C': [0, 1],
            'D': [0, 1]
        }
        schedule = Schedule(n_weekdays=1, n_slots_day=2, n_tracks=2,
                            n_rooms=2, courses=courses)
        schedule.schedule[0, 0, 0] = 'A'
        schedule.schedule[0, 0, 1] = 'B'
        schedule.schedule[0, 1, 0] = 'C'
        schedule.schedule[0, 1, 1] = 'D'
        return schedule

    @staticmethod
    def get_one_day_schedule_intervals() -> typing.Tuple[Schedule, typing.List[int]]:
        courses = {
            'A': [0, 1],
            'B': [0],
            'C': [1],
            'D': [0],
            'E': [0, 1],
        }
        schedule = Schedule(n_weekdays=1, n_slots_day=8, n_tracks=2,
                            n_rooms=1, courses=courses)
        schedule.schedule[0, 1, 0] = 'A'
        schedule.schedule[0, 2, 0] = 'B'
        schedule.schedule[0, 3, 0] = 'C'
        schedule.schedule[0, 4, 0] = 'D'
        schedule.schedule[0, 5, 0] = 'E'
        return schedule, [1, 2]

    @staticmethod
    def get_one_day_schedule_intervals_2rooms() -> typing.Tuple[Schedule, typing.List[int]]:
        courses = {
            'A': [0],
            'B': [0],
            'C': [0],
            'D': [0],
            'E': [0],
        }
        schedule = Schedule(n_weekdays=1, n_slots_day=8, n_tracks=1,
                            n_rooms=2, courses=courses)
        # note that this schedule is illegal, but a good way to test the room counting
        schedule.schedule[0, 1, 0] = 'A'
        schedule.schedule[0, 2, 1] = 'B'
        schedule.schedule[0, 4, 0] = 'C'
        schedule.schedule[0, 4, 1] = 'D'
        schedule.schedule[0, 6, 0] = 'E'
        return schedule, [2]

    @staticmethod
    def get_schedule_four_tracks() -> Schedule:
        courses = {
            'A': [0, 1, 2],
            'B': [0, 1],
            'C': [1, 2, 3],
            'D': [3],
            'E': [2, 3],
            'F': [0],
        }
        schedule = Schedule(n_weekdays=1, n_slots_day=3, n_tracks=4,
                            n_rooms=2, courses=courses)
        return schedule

    @staticmethod
    def get_schedule_four_tracks_2courses() -> Schedule:
        courses = {
            'A': [0, 1, 2],
            'B': [0, 1],
            'C': [1, 2, 3],
            'D': [3],
            'E': [2, 3],
            'F': [0],
        }
        schedule = Schedule(n_weekdays=2, n_slots_day=3, n_tracks=4,
                            n_rooms=2, courses=courses)
        return schedule

    @staticmethod
    def get_schedule_impossible() -> Schedule:
        courses = {
            'A': [0, 1, 2],
            'B': [0, 1],
            'C': [1, 2, 3],
            'D': [3],
            'E': [2, 3],
            'F': [0],
        }
        schedule = Schedule(n_weekdays=2, n_slots_day=2, n_tracks=4,
                            n_rooms=1, courses=courses)
        return schedule


class TestSchedule(unittest.TestCase):

    def test_print_schedule(self):
        schedule, _ = ScheduleFactory.get_one_day_schedule()
        # prints total schedule
        schedule.print_schedule(None)
        for track in range(schedule.n_tracks):
            schedule.print_schedule(track)

    def test_count_courses_on_day(self):
        schedule, courses_days = ScheduleFactory.get_one_day_schedule()

        for track, courses_day in zip(range(schedule.n_tracks), courses_days):
            result = schedule.count_courses_on_day(0, track)
            self.assertEqual(courses_day, result)

    def test_duplicate_track_courses_on_slot(self):
        schedule, _ = ScheduleFactory.get_one_day_schedule()

        for slot in range(schedule.n_slots_day):
            for track in range(schedule.n_tracks):
                result = schedule.duplicate_track_courses_on_slot(0, slot, track)
                self.assertFalse(result)

    def test_duplicate_track_courses_on_slot_duplicates(self):
        schedule = ScheduleFactory.get_one_day_schedule_duplicates()

        for slot in range(schedule.n_slots_day):
            for track in range(schedule.n_tracks):
                result = schedule.duplicate_track_courses_on_slot(0, slot, track)
                self.assertTrue(result)

    def test_count_intervals_on_day(self):
        schedule, intervals = ScheduleFactory.get_one_day_schedule_intervals()

        for track, interval in zip(range(schedule.n_tracks), intervals):
            result = schedule.count_intervals_on_day(0, track)
            self.assertEquals(interval, result)

    def test_count_intervals_on_day_2rooms(self):
        schedule, intervals = ScheduleFactory.get_one_day_schedule_intervals_2rooms()

        for track, interval in zip(range(schedule.n_tracks), intervals):
            result = schedule.count_intervals_on_day(0, track)
            self.assertEquals(interval, result)

    def _check_solution(self, schedule: Schedule, result: np.array):
        self.assertIsNotNone(result)
        result_flat = result.flatten()
        result_flat = np.delete(result_flat, np.where(result_flat == ''))
        # no duplicates
        self.assertEqual(len(np.unique(result_flat)), len(result_flat))
        # all courses
        self.assertSetEqual(set(result_flat), set(schedule.courses.keys()))

        for day in range(schedule.n_weekdays):
            for track in range(schedule.n_tracks):
                self.assertNotEqual(schedule.count_courses_on_day(day, track), 1)
                self.assertLessEqual(schedule.count_intervals_on_day(day, track), 1)

                for slot in range(schedule.n_slots_day):
                    self.assertFalse(schedule.duplicate_track_courses_on_slot(day, slot, track))

    def test_build_schedule_backtracking(self):
        # test case that fails when attempting greedy
        schedule = ScheduleFactory.get_schedule_four_tracks()
        result = schedule.build_schedule_backtracking()
        self._check_solution(schedule, result)

    def test_build_schedule_backtracking_2courses_day(self):
        # test case that attempts to make the 2 courses per day rule fail
        schedule = ScheduleFactory.get_schedule_four_tracks_2courses()
        result = schedule.build_schedule_backtracking()
        self._check_solution(schedule, result)

    def test_build_schedule_impossible(self):
        # test case that attempts to make the 2 courses per day rule fail
        schedule = ScheduleFactory.get_schedule_impossible()
        result = schedule.build_schedule_backtracking()
        self.assertIsNone(result)
