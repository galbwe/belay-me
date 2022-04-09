from ..model import Gym


class GymRepository:
    def __init__(self, session):
        self.session = session

    def add(self, gym: Gym):
        self.session.add(gym)

    def get(self, name):
        return self.session.query(Gym).filter_by(name=name).first()

    def list(self):
        return self.session.query(Gym).all()
