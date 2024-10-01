# from sqlalchemy import Column, Integer, String
# from app.database import Base

# Base.metadata.clear()

# class UploadImage(Base):
#     __tablename__ = "upload_image"
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     image_path = Column(String(255), index=True, extend_existing=True)

# __table_args__ = {'extend_existing': True}