from sphere import db


class ExternalService(db.Model):
    """ Название внешней экспертизы, которая по убытку работы производит """

    __tablename__ = 'base_external_service'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))

    def __str__(self):
        return self.title
