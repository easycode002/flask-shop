from app.models import User
from app import db
from datetime import datetime

class UserService:
    @staticmethod
    def get_all_users():
        """Method to get all user"""
        return User.query.filter_by(isDeleted=False).all()
    
    @staticmethod
    def create_user(name):
        """Method to add new user"""
        try:
            user=User(name=name)
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Failded to create user :{e}")
    
    @staticmethod
    def get_total_user():
        """Method to get total users"""
        return User.query.filter_by(isDeleted=False).count()
    
    @staticmethod
    def get_user_by_name(name):
        """Check if a uuser already exsit by name"""
        return User.query.filter_by(name=name,isDeleted=False).first()
    
    @staticmethod
    def get_user_by_id(user_id):
        """Method to get user via id"""
        return User.query.filter_by(id=user_id,isDeleted=False).first()
    
    @staticmethod
    def trask_users(user_id=None):
        """"Method to get user after soft-delete
            - if `user_id` is provided, return a specific soft-delete user.
            - if no `user_id` is provided, return all soft-delete users.
        """
        query=User.query.filter_by(isDeleted=True)
        if user_id:
            return query.filter_by(id=user_id).first()
        
        return query.all()
    
    @staticmethod
    def update_user(user_id,name):
        """"Update user name"""
        user=UserService.get_user_by_id(user_id)
        if not user or user.isDeleted:
            return None
        user.name=name
        user.updatedAt=datetime.utcnow()
        db.session.commit()
        return user
    
    @staticmethod
    def soft_delete_user(user_id):
        """Softdelete user => mark isDeleted=True"""
        user=UserService.get_user_by_id(user_id)
        if not user or user.isDeleted:
            return None
        else:
            user.isDeleted=True
            user.deletedAt=datetime.utcnow()
            db.session.commit()
            return user
        
    @staticmethod
    def restore_user(user_id):
        """Restore user(mark isDelete=False)"""
        user=UserService.trask_users(user_id)
        if not user or user.isDeleted==False:
            return None
        else:
            user.isDeleted=False
            user.deletedAt=None
            db.session.commit()
            return user
        
    @staticmethod
    def permanent_delete_user(user_id):
        try:
            """Permanent delete user from database"""
            user=UserService.get_user_by_id(user_id)
            if not user or user.id==None:
                return None
            else:
                db.session.delete(user)
                db.session.commit()
                return True
        except Exception as e:
            raise ValueError(f"Failed to delete user :{e}")
        