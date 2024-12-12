from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc
from app.db import session
from app.db.models import Posts
from math import ceil

class PostsDao:

    def __init__(self):
        self.db = session

    def create_posts(self, posts_data: dict):
        try:
            existing_posts = self.db.query(Posts).filter(Posts.url_sid == posts_data['url_sid']).first()
            if not existing_posts:
                new_posts = Posts(**posts_data)
                self.db.add(new_posts)
                self.db.commit()
                self.db.refresh(new_posts)
                return new_posts.to_dict()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"An error occurred while creating the challenge: {str(e)}")

    def delete_posts(self, posts_id: int):
        posts = self.db.query(Posts).filter(Posts.id == posts_id).first()
        if posts:
            self.db.delete(posts)
            self.db.commit()
            return True
        return False

    def get_posts(self, posts_id: int):
        posts = self.db.query(Posts).filter(Posts.id == posts_id).first()
        return posts.to_dict() if posts else None

    def get_posts_by_url_sid(self, url_sid: str):
        posts = self.db.query(Posts).filter(Posts.url_sid == url_sid).first()
        return posts.to_dict() if posts else None

    def page(self, page: int, size: int, title, category):
        # 构建基础查询
        query = self.db.query(Posts)

        # 如果提供了 title 参数，则添加到查询条件中
        if title:
            query = query.filter(Posts.title.ilike(f"%{title}%"))

        # 如果提供了 category 参数，则添加到查询条件中
        if category:
            query = query.filter(Posts.category == category)

        # 计算总记录数
        total = query.count()

        # 如果没有记录，直接返回空列表
        if total == 0:
            return {
                'items': [], 'total': 0, 'page': page, 'size': size, 'pages': 0
            }

        # 计算总页数
        pages = ceil(total / size)

        if page > pages:
            page = pages

        offset = (page - 1) * size
        posts_query = query.order_by(desc(Posts.published_at)).offset(offset).limit(size)
        posts_items = posts_query.all()

        return {
            'items': [item.to_dict() for item in posts_items], 'total': total, 'page': page, 'size': size, 'pages': pages
        }