from . import MLModel, db


class ImageModel(MLModel):

    __tablename__ = "image_table"

    id = db.Column(db.BIGINT, primary_key=True)
    image_content = db.Column(db.String, nullable=False)

    def __init__(self, data):
        super().__init__(data)
        self.id = data.get('id')
        self.image_content = data.get('image_content')

    @staticmethod
    def get_all_images(all_args):
        if 'id' in all_args:
            return ImageModel.query.filter(ImageModel.id == all_args.get('id'))
        return ImageModel.query.all()

    @staticmethod
    def get_one_image(id):
        return ImageModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)
