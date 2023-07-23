# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class Flashcard(Base):
    __tablename__ = 'flashcard'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    box = Column(Integer)


class MemorizationTool:
    def __init__(self, card_set, how_many_boxes):
        self.menu_ = {
            'main':          {'1': ('1. Add flashcards', self.menu, 'add_card'),
                              '2': ('2. Practice flashcards', self.practice, ''),
                              '3': ('3. Exit', exit, '')},
            'add_card':      {'1': ('1. Add a new flashcard', self.add_new, ''),
                              '2': ('2. Exit', self.menu, 'main')},
            'practice_menu': {'y': ('press "y" to see the answer:', self.see_answer, '\n'),
                              'n': ('press "n" to skip:', self.skip, ''),
                              'u': ('press "u" to update:', self.menu, 'update_menu')},
            'if_correct':    {'y': ('press "y" if your answer is correct:', self.move_box, 'y'),
                              'n': ('press "n" if your answer is wrong:', self.move_box, 'n')},
            'update_menu':   {'d': ('press "d" to delete the flashcard:', self.delete_, ''),
                              'e': ('press "e" to edit the flashcard:', self.edit_, '')}
        }
        self.box_max_number = how_many_boxes
        self.session = self.go_through_sessions(self.box_max_number)
        self.engine = create_engine(f'sqlite:///{card_set}?check_same_thread=False')
        Base.metadata.create_all(self.engine)
        self.flashcards = sessionmaker(bind=self.engine)()
        self.card = self.flashcards.query(Flashcard)
        self.current_ = None

    @staticmethod
    def go_through_sessions(box_max_number):
        session = 0
        while True:
            session = session + 1 if session < box_max_number else 1
            yield session

    def menu(self, name):
        menu_msg = '\n'.join(f'{option[0]}' for option in self.menu_[name].values()) + '\n'
        while (option := input(menu_msg)) not in self.menu_[name]:
            print(f'{option} is not an option')
        return self.menu_[name][option][1](self.menu_[name][option][2])

    def add_new(self, none):
        while not (q := input('\nQuestion:\n').strip()): continue
        while not (a := input('Answer:\n').strip()): continue
        self.flashcards.add(Flashcard(question=q, answer=a, box=1))
        self.flashcards.commit()
        return self.menu('add_card')

    def practice(self, enter):
        # for i in range(1, 5):
        #     print('box' + str(i), self.card.filter(Flashcard.box == i).all(), self.card.filter(Flashcard.box == i).count())
        if self.card.filter(Flashcard.box <= self.box_max_number).count() == 0:
            self.current_ = None
            print('There is no flashcard to practice!')
        else:
            current_session = next(self.session)
            while self.card.filter(Flashcard.box <= current_session).count() == 0:
                current_session = next(self.session)
            else:
                for card in self.card.filter(Flashcard.box <= current_session).all():
                    print('\nQuestion:', card.question)
                    self.current_ = self.card.filter(Flashcard.id == card.id)
                    self.menu('practice_menu')
        print(enter)
        return self.menu('main')

    def see_answer(self, enter):
        print('\nAnswer: ' + self.current_.one().answer, end=enter)
        return self.menu('if_correct')

    def move_box(self, correct):
        # print('box from', self.current_.one().box, end=' ')
        self.current_.update({"box": self.current_.one().box + 1 if correct == 'y'
                                                                 else max(self.current_.one().box - 1, 1)})
        self.flashcards.commit()
        # print('to', self.current_.one().box)

    def skip(self, none):
        pass

    def delete_(self, card):
        self.current_.delete()
        self.flashcards.commit()

    def edit_(self, card):
        if new_q := input(f'\ncurrent question:{self.current_.one().question}\nplease write a new question:\n'):
            self.current_.update({"question": new_q})
        if new_a := input(f'\ncurrent answer:{self.current_.one().answer}\nplease write a new answer:\n'):
            self.current_.update({"answer": new_a})
        self.flashcards.commit()

try:
    MemorizationTool('flashcard2.db', 3).menu('main')
finally:
    print('Bye!')
