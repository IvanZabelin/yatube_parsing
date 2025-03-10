import datetime as dt

from scrapy.exceptions import DropItem
from sqlalchemy import create_engine, Column, Integer, String, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session



Base = declarative_base()


class MondayPost(Base):
    __tablename__ = 'monday_post'
    id = Column(Integer, primary_key=True)
    author = Column(String(200))
    date = Column(Date)
    text = Column(Text)


class MondayPipeline:

    def open_spider(self, spider):
        engine = create_engine('sqlite:///sqlite.db')
        Base.metadata.create_all(engine)
        self.session = Session(engine)

    def process_item(self, item, spider):
        post_date = dt.datetime.strptime(item['date'], '%d.%m.%Y')
        if post_date.weekday() == 0:  # 0 — понедельник
            monday_post = MondayPost(
                author=item['author'],
                date=post_date,
                text=item['text']
            )
            self.session.add(monday_post)
            self.session.commit()
            return item

    def close_spider(self, spider):
        self.session.close()
