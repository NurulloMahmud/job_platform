from sqlalchemy import Column, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.session import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    message = Column(Text, nullable=False)

    __table_args__ = (UniqueConstraint("user_id", "job_id", name="uq_user_job"),)

    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")
