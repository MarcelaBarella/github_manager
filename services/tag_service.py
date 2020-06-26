from domain.tag import Tag

class TagService:
    def __init__(self, tag, db_session):
        self.tag = tag
        self.db_session = db_session

    def get(self):
        formated_tag = self.tag.capitalize()
        new_tag = Tag().query.filter_by(name=formated_tag).first()
        if tag is None:
            new_tag = Tag()
            new_tag.name = formated_tag
        
            self.db_session.commit()
