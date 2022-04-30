from ..model import Gym, Activity


class GymRepository:
    def __init__(self, session):
        self.session = session

    def add(self, gym: Gym):
        self.session.add(gym)

    def get(self, name):
        return self.session.query(Gym).filter_by(name=name).first()

    def list(self):
        return self.session.query(Gym).all()


class ActivityRepository:
    def __init__(self, session):
        self.session = session

    def get(self, name):
        return self.session.query(Activity).filter_by(name=name).first()

    def list(self, names=None):
        if names is not None:
            return self.session.query(Activity).filter(Activity.name.in_(names)).all()
        return self.session.query(Activity).all()
