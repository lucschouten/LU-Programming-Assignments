import numpy as np
import typing

class Schedule(object):

    def __init__(self, n_weekdays: int, n_slots_day: int, n_rooms: int,
                 n_tracks: int, courses: typing.Dict[str, typing.List[int]]):
        """
        Data structure containing all information and functions required for
        building a schedule

        :param n_weekdays: the number of days in the week that this schedule can
        span
        :param n_slots_day: the number of time-slots in a day on which courses
        can be scheduled
        :param n_rooms: The number of rooms that this schedule can span
        :param n_tracks: The number of tracks that are being offered in the
        schedule
        :param courses: A dict of the courses. The key is of type string (the
        name), and the value is a list containing integers, each integer
        representing a track that has to follow this course. For each course,
        it is guaranteed that it belongs to at least one track.
        """
        self.n_weekdays = n_weekdays
        self.n_slots_day = n_slots_day
        self.n_rooms = n_rooms
        self.n_tracks = n_tracks
        self.courses = courses
        self.schedule = np.empty(shape=(n_weekdays, n_slots_day, n_rooms), dtype=str)

    def print_schedule(self, track: typing.Optional[int]) -> None:
        """
        Prints a schedule, in free format

        :param track: if track is given (not None), the schedule will only
        contain courses belonging to a given track
        """
        schedule = np.empty(shape=(self.n_weekdays, self.n_slots_day, 1), dtype=str) #initialize empty schedule
        if track is not None: #If only the schedule for a certain track should be printed 
            for weekday in range(len(self.schedule)):
                for timeslot in range(len(self.schedule[weekday])):
                    for course in range(len(self.schedule[weekday][timeslot])): #loop trough self.schedule
                        if len(self.schedule[weekday][timeslot][course]) > 0:
                            if track in self.courses.get(self.schedule[weekday][timeslot][course]):
                                #If track in course in room in self.schedule.
                                schedule[weekday][timeslot] = self.schedule[weekday][timeslot][course] #Put the course followed by track in track schedule. 
        if track is None:
            schedule = self.schedule

        for index_weekday, weekday in enumerate(schedule):  
            print("Weekday " + str(index_weekday + 1) + ": \n" )
            for index_timeslot, timeslot in enumerate(weekday):
                print("        Timeslot " + str(index_timeslot + 1) +":") #print schedule in formatted way.
                print("        Courses: ", end ='')
                for course in timeslot:
                    print(str(course) +' ' , end= '')
                print("\n")
            print("")


    def count_courses_on_day(self, day: int, track: int) -> int:
        """
        Counts the number of courses a given track has on a given day

        :param day: the day to check
        :param track: the track to check
        :return: The number of courses beloging to that track
        """
        number_of_courses = 0
        for slot in self.schedule[day]:
            for course in slot:
                if len(course) > 0:
                    if track in self.courses.get(course):
                        number_of_courses += 1
                        
        return number_of_courses

    def duplicate_track_courses_on_slot(self, day: int, slot: int,
                                        track: int) -> bool:
        """
        Checks whether for a given slot on a given day, a duplicate entrees exist for a given track.

        :param day: the day to check
        :param slot: the slot to check
        :param track: the track to check

        :return: True if there are duplicates, False otherwise
        """
        duplicates = -1
        for course in self.schedule[day][slot]:
            if course != "":
                tracks_in_course = self.courses.get(course)
                if track in tracks_in_course:
                    duplicates += 1

        if duplicates >= 1:
            return True
        else: 
            return False

    def count_intervals_on_day(self, day: int, track: int) -> int:
        """
        Counts the number of interval slot for a track on a given day. A slot s
        is considered an interval slot if there exists a pair of slots (b,e)
        that also offer a course in that track, such that b < s < e.

        :param day: The day to check
        :param track: The track to check

        :return: Returns the number of intervals for a given track on a day.
        """
        in_interval = False
        counter_of_intervals = 0
        total_number_of_intervals = 0
        for timeslot in self.schedule[day]:
            track_in_course_in_timeslot = False
            for course in timeslot:                
                if len(course) > 0: #Room has a course
                    if track in self.courses.get(course):
                        track_in_course_in_timeslot = True

            if track_in_course_in_timeslot is True: #A course is found in the past time slot that is followed by the specified track.
                if in_interval is False: #If we aren't in an interval yet, meaning that we haven't had a course in an earlier timeslot, we switch our state to being in an interval.
                    in_interval = True
                elif in_interval == True: #If we already are in an interval and we find a potential ending, meaning we find a course that we follow with our track, we add the intervals to the total amount of intervals.
                    total_number_of_intervals += counter_of_intervals
                    counter_of_intervals = 0

            elif track_in_course_in_timeslot is False: #No course is found in the past time slot. So we check if we were in an interval, if so we add to the counter
                if in_interval == True:
                    counter_of_intervals += 1

        return total_number_of_intervals

    def final_check(self) -> bool:
        """ Determines if a track has atleast 2 courses on a day when it has a course on a day.
        Returns: A boolean, True if the schedule has at least two courses on a day
        the track has courses, False otherwise. """

        for day in range(self.n_weekdays):
            for track in range(self.n_tracks):
                if self.count_courses_on_day(day, track) < 2 and self.count_courses_on_day(day, track) != 0: 
                    return False
                    
        return True 
        
    def violatesrules(self) -> bool:
        
        """Checks whether the 'given schedule' violates one of the following conditions:
        - There is at most one interval hour for each track.
        - Two courses that are offered to the same track are not offered in the same time slot.

        Returns: True if one of these conditions is violated, False otherwise.
        """
        for day in range(self.n_weekdays):
            for track in range(self.n_tracks):

                if self.count_intervals_on_day(day, track) > 1:
                    return True
                for slot in range(self.n_slots_day):
                    if self.duplicate_track_courses_on_slot(day, slot, track):
                        return True

        return False

    def _build_schedule_recursive(
            self, start_day: int, start_slot: int, start_room: int,
            courses: typing.Dict[str, typing.List[int]]) -> np.array:
        """
        Function that builds a schedule using backtracking.
        The function checks if the schedule complies with the following rules:

        - There is at most one interval hour for each track.
        - Two courses that are offered to the same track are not offered in the same time slot.
        - Each course should be offered exactly once in the schedule
        - When courses are offered for a track on a certain day, there should be at least two courses that day.

        :param start_day: the index (int) of the day that has to be checked.
        :param start_slot: the index (int) of the slot that has to be checked.
        :param start_room: the index (int) of the room that has to be checked.
        :param courses: dictionary countaining the courses that haven't been placed in the schedule yet.
        
        returns: A schedule that complies with the rules mentioned above, None otherwise.
        """
        if len(courses) == 0:
            if self.final_check() is True:
                return self.schedule
            else:
                return None
        #The three if statements below are to check the day, slot and room boundaries.
        #It makes sure the recursive function stays within the boundaries of the schedule.
        if start_day >= self.n_weekdays:
            return None
        if start_slot >= self.n_slots_day:
            start_room = 0
            start_slot = 0
            start_day += 1
            return self._build_schedule_recursive(start_day, start_slot, start_room, courses)
        if start_room >= self.n_rooms:
            start_room = 0
            start_slot += 1
            return self._build_schedule_recursive(start_day, start_slot, start_room, courses)

        for course in courses:
            self.schedule[start_day, start_slot, start_room] = course            
            copy_courses = courses.copy()
            copy_courses.pop(course)

            if self.violatesrules() is False:
                result = self._build_schedule_recursive(start_day, start_slot, start_room + 1, copy_courses) #Calls itself with the next room to check.
                if type(result) is not None: #True when a schedule is returned.                
                    return result
            self.schedule[start_day, start_slot, start_room] = ""
            
        if self.violatesrules() is False:
            result2 = self._build_schedule_recursive(start_day, start_slot, start_room + 1, courses)
            if type(result2) is not None:
                return result2    
        return None #Returns None because there is no schedule that doesn't violate the rules.

    def build_schedule_backtracking(self) -> np.array:
        """
        Function that builds a schedule using backtracking. Make sure to make
        use of the functions that check the validity of the schedule throughout.
        If you encounter a schedule that you already know to be invalid, you
        should backtrack and try another option.
        This function can be implemented by a single call to another function,
        _build_schedule_recursive. You are allowed to change the argumentes of
        the function _build_schedule_recursive

        :return: a valid schedule if such exists, None otherwise
        """ 
        return self._build_schedule_recursive(0, 0, 0, self.courses)

    def build_schedule_greedy(self) -> np.array:
        """
        Function that iteratively builds a schedule in a greedy way. 
        The function finds a most contrained room and places a course,
        with the least amount of options in the schedule, in the schedule on the most constrained room.

        :return: a schedule that attempts to respect the rules as much as possible.
        """
        copy_courses = self.courses.copy()      

        def place_course_most_constrained_room():
            """
            Uses the 'Most Constrained Variable' heuristic to find the room within the
            course with the least allowed possible courses by trying out every course 
            on each room. After the room that allows for the least amount of courses is found, 
            the course to put there is determined by determine_best_course() and put at that room. 
            """

            possible_rooms_for_course = {}
            for course in self.courses:
                possible_rooms_for_course[course] = 0

            lowest_found_possiblities = float("inf")
            #Loops through the schedule.
            for weekday in range(len(self.schedule)):
                for timeslot in range(len(self.schedule[weekday])):
                    for room in range(len(self.schedule[weekday][timeslot])): 
                        possible_courses_for_room = 0 
                        possible_courses_room = []
                        for course in copy_courses:
                            copy_room_value = self.schedule[weekday][timeslot][room] 
                            if copy_room_value == '':
                                self.schedule[weekday][timeslot][room] = course #Try every course in all emtpy rooms.
                                if self.violatesrules() == False:
                                    possible_courses_for_room += 1 #Increase the number of courses which can be given in a room. 
                                    possible_rooms_for_course[course] +=1 #increase the amount of times a course can be given in the schedule.
                                    possible_courses_room.append(course)
                            self.schedule[weekday][timeslot][room] = copy_room_value
                        #If a room is found where less courses can be given compared to the previous room with the least courses.
                        if (possible_courses_for_room < lowest_found_possiblities) and possible_courses_for_room > 0:
                            lowest_found_possibilities = possible_courses_for_room
                            most_constrained_room = (weekday, timeslot, room)
                            courses_most_constraind_room = possible_courses_room
                                        
            if 'most_constrained_room' in locals(): #Checks if variabele 'most_constrained_room' is initialised.
                '''Determines the best course for the most constrained_room by determining
                which course, that can be placed within the most constrained room, can be given
                in the least amount of rooms in the whole schedule.'''
                possibilities_most_constrained_course = float("inf")
                best_course = None 
                for course in courses_most_constraind_room:
                    if (possible_rooms_for_course.get(course) < possibilities_most_constrained_course) and (possible_rooms_for_course.get(course) > 0):
                        best_course = course 
                self.schedule[most_constrained_room] = best_course 
                    
                copy_courses.pop(best_course)
            else:
    
                return self.schedule #There is no move left which does not break rules. 
        

        counter = 0
        while counter < self.n_weekdays*self.n_slots_day*self.n_rooms: #Place courses until all the rooms are full.
            place_course_most_constrained_room()
            counter += 1
        return self.schedule 
