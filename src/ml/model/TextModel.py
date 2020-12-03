from . import MLModel, db


class TextModel(MLModel):

    __tablename__ = "text_table"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    text_content = db.Column(db.Text, nullable=False)

    def __init__(self, data):
        super().__init__(data)
        self.text_content = data.get('text_content')

    @staticmethod
    def get_all_text(all_args):
        if 'id' in all_args:
            return TextModel.query.filter(TextModel.id == all_args.get('id'))
        return TextModel.query.all()

    @staticmethod
    def get_one_text(id):
        return TextModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)
