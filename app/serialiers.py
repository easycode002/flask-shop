from app.utils import format_datetime

def serialize_user(user):
    """Convert a user object to dist with format date"""
    return {
        'id':user.id,
        'name':user.name,
        'createdAt':format_datetime(user.createdAt),
        'updatedAt':format_datetime(user.updatedAt),
        'deletedAt':format_datetime(user.deletedAt),
        'isDeleted':user.isDeleted
    }