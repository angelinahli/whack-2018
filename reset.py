from app import db
from app.models import User

for user_id in [1, 2]:
    User.query.get(user_id).last_action = "NONE"
    User.query.get(user_id).has_onboarded = False

db.session.commit()
db.session.close()

print("All done!")
