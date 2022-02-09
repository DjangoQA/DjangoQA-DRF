from datetime import datetime


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/users/avatars/user_<id>
    filename = f'user_{instance.id}_{int(datetime.now().timestamp())}.{filename.split(".")[-1]}'
    return f'users/avatars/{filename}'
