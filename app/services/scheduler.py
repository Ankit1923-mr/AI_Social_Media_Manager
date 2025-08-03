# scheduler.py

import random
import json
from collections import OrderedDict
import os

WEEKDAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

# Removed emoji prefixes from templates
POST_TEMPLATES = [
    "Tip of the week: Engage with your audience through stories.",
    "Quote of the day: 'Success is no accident.'",
    "User spotlight: Check out this amazing post by @user!",
    "Enjoy 20% off all items this weekend!",
    "Quick Fix: Use hashtags smartly to boost visibility.",
    "Trending Now: Explore what's hot in your niche.",
    "Behind the Scenes: A look at our team’s workflow.",
    "Giveaway: Participate to win exciting prizes!",
    "Announcement: New product launch this Thursday!",
    "Poll: What type of content do you want next?"
]

SCHEDULE_FILE = "weekly_schedule.json"

class WeeklyScheduler:
    def __init__(self):
        self.weekly_schedule = self.load_schedule()

    def load_schedule(self):
        if os.path.exists(SCHEDULE_FILE):
            with open(SCHEDULE_FILE, 'r') as f:
                return OrderedDict(json.load(f))
        return OrderedDict()

    def save_schedule(self):
        with open(SCHEDULE_FILE, 'w') as f:
            json.dump(self.weekly_schedule, f)

    def generate_schedule(self, post_frequency, preferred_days):
        preferred_days = [day for day in WEEKDAYS if day in preferred_days]
        if post_frequency > len(preferred_days):
            raise ValueError("Post frequency exceeds number of preferred days.")

        # Choose days and templates
        chosen_days = random.sample(preferred_days, post_frequency)
        chosen_templates = random.sample(POST_TEMPLATES, post_frequency)

        # Build a fresh schedule dict (no update)
        schedule = {day: msg for day, msg in zip(chosen_days, chosen_templates)}

        # Sort by weekday order and assign
        self.weekly_schedule = OrderedDict(
            sorted(schedule.items(), key=lambda x: WEEKDAYS.index(x[0]))
        )

        self.save_schedule()
        return self.weekly_schedule

    def get_schedule(self):
        return self.weekly_schedule

    def update_post(self, day, content):
        if day not in self.weekly_schedule:
            raise KeyError(f"No scheduled post for {day}")
        self.weekly_schedule[day] = content
        self.save_schedule()
        return self.weekly_schedule

    def delete_post(self, day):
        if day not in self.weekly_schedule:
            raise KeyError(f"No scheduled post for {day}")
        del self.weekly_schedule[day]
        self.save_schedule()
        return self.weekly_schedule

    def reset_schedule(self):
        self.weekly_schedule = OrderedDict()
        self.save_schedule()
