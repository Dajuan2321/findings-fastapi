from sqlalchemy import Column, String, Text, Integer, DateTime

from app.db import Base

class Posts(Base):
    __tablename__ = 'crawl_posts'

    id = Column(Integer, primary_key=True, index=True)
    xid = Column(String, index=True)
    title = Column(String)
    thumbnail = Column(Text)
    description = Column(String)
    content = Column(Text)
    url = Column(String)
    url_sid = Column(String)
    source = Column(String)
    publisher = Column(String)
    category = Column(String)
    views = Column(Integer, default=0)
    logo = Column(Text)
    published_at = Column(DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'xid': self.xid,
            'title': self.title,
            'thumbnail': self.thumbnail,
            'description': self.description,
            'content': self.content,
            'url': self.url,
            'url_sid': self.url_sid,
            'source': self.source,
            'publisher': self.publisher,
            'category': self.category,
            'logo': self.logo,
            'views': self.views,
            'published_at': self.published_at.strftime('%Y-%m-%d %H:%M:%S') if self.published_at else None,
        }