# coding: UTF-8

from bourjois.models.database import Base, engine


if __name__ == '__main__':
    Base.metadata.create_all(engine)