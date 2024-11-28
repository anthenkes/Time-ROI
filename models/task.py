import inspect
from typing import Optional

class Metrics:
    def __init__(self, immediate_benefit: int, future_impact: int, personal_fulfillment: int, progress: int):
        self.immediate_benefit = int(immediate_benefit)
        self.future_impact = int(future_impact)
        self.personal_fulfillment = int(personal_fulfillment)
        self.progress = self.normalize_progress(progress)
    
    def normalize_progress(self, progress: int) -> int:
        """Normalize progress percentage to a scale of 1 to 5."""
        if 0 <= progress < 20:
            return 1
        elif 20 <= progress < 40:
            return 2
        elif 40 <= progress < 60:
            return 3
        elif 60 <= progress < 80:
            return 4
        elif 80 <= progress <= 100:
            return 5
        else:
            raise ValueError("Progress must be between 0 and 100.")


    def calculate_output_score(self):
        total = sum(value for name, value in vars(self).items() if isinstance(value, int))
        return total / self._get_metrics_count()

    def calculate_roi(self, time_investment: int, output_score: Optional[int] =None):
        # Example calculation for ROI
        if output_score is not None:
            return output_score / time_investment
        return (self.calculate_output_score()) / time_investment

    @staticmethod
    def _get_metrics_count():
        metrics = inspect.signature(Metrics).parameters
        return len(metrics)
class Task:
    def __init__(self, date: str, task: str, category: str, time_investment: int, start_time: str, end_time: str,
                 immediate_benefit: int, future_impact: int, personal_fulfillment: int, progress: int,
                 notes: str = ""):
        self.date = date
        self.task = task
        self.category = category
        self.time_investment = time_investment
        self.start_time = start_time
        self.end_time = end_time
        self.notes = notes

        self.metrics = Metrics(immediate_benefit, future_impact, personal_fulfillment, progress)
        self.output_score = self.metrics.calculate_output_score()
        self.roi = self.metrics.calculate_roi(time_investment, self.output_score)

    def to_tuple(self):
        return (self.date, self.task, self.category, self.time_investment, self.start_time, self.end_time,
                self.metrics.immediate_benefit, self.metrics.future_impact, self.metrics.personal_fulfillment, self.metrics.progress,
                self.output_score, self.roi, self.notes)

    def validate(self):
        #TODO: Add validation logic here
        if not self.date or not self.task or not self.time_investment:
            raise ValueError("Date,task and time investment time are required fields.")
        # Add more validation as needed

    def __str__(self):
        return f"Task({self.task}, {self.date}, {self.category})"
