class Task:
    def __init__(self):
        self.number = 0
        self.question = ''
        self.answers = []
        self.answer_i = 0
        self.is_answer_multi = False
        self.comment = ''
        self.has_picture = False
        self.full_path_picture = ''

    def set_picture(self, full_path):
        self.full_path_picture = full_path
        self.has_picture = True
