"""
Utils
"""

def room_upload_path(instance, filename):
    """ Returns the upload path with the idk """
    return f"images/rooms/{instance.id}/{filename}"
