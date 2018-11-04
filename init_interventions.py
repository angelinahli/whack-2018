from app import db
from app.models import Intervention

interventions = [
    "This exercise helps you cultivate gratitude! Grab some pen and paper, " \
    + "and write down three things that have gone particularly well for you " \
    + "today. These can be big or small, such as 'ate some great food' or " \
    + "'spent time with a loved one'. Try to include a reason why each good " \
    + "thing happened.",

    "Movement is great for the body! If you can, take 5 minutes to move " \
    + "around for a little. Some ideas: Get up and take a mindful walk, " \
    + "practice your badass chair dance moves, or flail about for bit. " \
    + "Anything goes!",

    "It's always nice to be around things that make you feel safe and happy! " \
    + "Expose yourself to something pleasing, such as the smell of your " \
    + "favorite perfume or the softness of a treasured blanket.",

    "I might be just a bot but I think humans under-appreciate appreciation " \
    + ":) Can you think of a time when someone in your life did something " \
    + "nice for you? Or, of someone who's an awesome human in general? Take " \
    + "this chance to tell that someone just how much you appreciate them! " \
    + "For instance, I appreciate YOU for your mental resillience!!"
]

for text in interventions:
    new_int = Intervention(text=text)
    db.session.add(new_int)

db.session.commit()
db.session.close()

print("All done!")
