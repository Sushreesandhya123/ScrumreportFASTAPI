# from sqlalchemy import Column, Integer, String
# from app.database import Base
# from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
# from sqlalchemy.orm import Session
# from app.modules.imageupload import UploadImage
# from app.database import get_db
# from fastapi.responses import JSONResponse, FileResponse
# import os
# import uuid

# class UploadImage(Base):
#     __tablename__ = "upload_image"
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     image_path = Column(String(255), index=True)

# router = APIRouter()

# @router.post("/upload/")
# async def upload_image(id: int = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
#     image_directory = "uploaded_images"
#     os.makedirs(image_directory, exist_ok=True)

#     # Generate a unique filename
#     file_extension = os.path.splitext(file.filename)[-1]
#     unique_filename = f"{uuid.uuid4()}{file_extension}"
#     file_location = os.path.join(image_directory, unique_filename)
    
#     # Save the uploaded file
#     with open(file_location, "wb+") as file_object:
#         file_object.write(file.file.read())

#     # Save the image record in the database
#     db_entity = UploadImage(id=id, image_path=file_location)
#     db.add(db_entity)
#     db.commit()
#     db.refresh(db_entity)

#     return {"id": db_entity.id, "image_path": db_entity.image_path}

# @router.get("/image/{image_id}")
# async def get_image(image_id: int, db: Session = Depends(get_db)):
#     db_entity = db.query(UploadImage).filter(UploadImage.id == image_id).first()
    
#     if not db_entity:
#         raise HTTPException(status_code=404, detail="Image not found")

#     image_path = db_entity.image_path
#     if not os.path.exists(image_path):
#         raise HTTPException(status_code=404, detail="File not found")

#     # Serve the image file directly
#     return FileResponse(image_path)

# @router.get("/images/")
# async def get_all_images(db: Session = Depends(get_db)):
#     images = db.query(UploadImage).all()
    
#     if not images:
#         raise HTTPException(status_code=404, detail="No images found")

#     image_data = [{"id": image.id, "image_path": image.image_path} for image in images]

#     return JSONResponse(content=image_data, status_code=200)
