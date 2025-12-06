# from cloudinary.uploader import upload
# from cloudinary.utils import cloudinary_url

# async def upload_avatar(file):
#     result = upload(file.file, folder="groupmatch/avatar")
#     return result.get("secure_url")


import cloudinary.uploader

async def upload_avatar(file):
    result = cloudinary.uploader.upload(
        file.file,
        folder="groupmatch/avatar"
    )
    return result.get("secure_url")
