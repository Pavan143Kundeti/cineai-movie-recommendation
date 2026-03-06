from sqlalchemy import Column, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from ..core.database import Base


class UserPreference(Base):
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    preferred_genres = Column(JSON, nullable=True)
    disliked_genres = Column(JSON, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="preferences")
