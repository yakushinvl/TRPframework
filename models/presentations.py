class Presentation:
    def __init__(self, id, event, student, title, duration, score_1, score_2):
        self.id = id
        self.event = event
        self.student = student
        self.title = title
        self.duration = duration
        self.score_1 = score_1
        self.score_2 = score_2
        self.total_score = self.calculate_total()
        self.result = self.get_result()

    def check_duration(self):
        if self.duration <= self.event.max_duration:
            return "в регламенте"
        return "превышен"

    def calculate_total(self):
        return round(self.score_1 + self.score_2, 2)

    def get_result(self):
        if self.total_score >= 9.0:
            return "1 место"
        elif self.total_score >= 8.0:
            return "2 место"
        elif self.total_score >= 7.0:
            return "3 место"
        else:
            return "участник"

    def __str__(self):
        status = self.check_duration()
        return (
            f"[{self.id}] {self.student.name} ({self.student.group}) | "
            f"мероприятие: {self.event.name} | "
            f"тема: {self.title} | "
            f"время: {self.duration} мин ({status}) | "
            f"балл: {self.total_score} | "
            f"результат: {self.result}"
        )


def create_presentation(presentations, event, student, title, duration, score_1, score_2):
    p = Presentation(len(presentations) + 1, event, student, title, duration, score_1, score_2)
    presentations.append(p)
    return p


def find_presbystud(presentations, query):
    q = query.lower()
    return [p for p in presentations if q in p.student.name.lower()]


def sort_presbyscore(presentations):
    return sorted(presentations, key=lambda p: p.total_score, reverse=True)


def find_presentation_by_id(presentations, presentation_id):
    for p in presentations:
        if p.id == presentation_id:
            return p
    return None
