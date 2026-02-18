from auth.database import SessionLocal
from users.models import User


db = SessionLocal()
db.query(User).update({User.daily_reports: 0})
db.commit()