# WHACK 2018

## To Do

* GOAL: Create a conversation flow between user and server to track mood daily.
    * How to send messages at a specific time per day?
    * How to create a flowchart that remembers what user said and asks them how they are doing now?
    * Write the flowchart of actions responding to the user.
    * Figure out how to store the users info somewhere.

* User prompted daily intervention:
    * User says "Hi" to start the conversation
    * INTRODUCTION: "Hi!" / something
    * ONBOARDING: IF this is the first time the user has contacted us, onboard them by giving them a short pitch about who we are and what we do.
        * Maybe have a flow dedicated to this.
    * CHECKIN: Ask the user how they are feeling today from a scale of 1-5.
    * RESPONSE: Respond appropriately to the user based on the scale.
    * ASKINTERVENTION: Ask the user whether they would like to try out an intervention now.
        * User can respond either "yes" or "no"
    * CHOOSEINTERVENTION: Select which intervention to introduce to the user, ask them to do something.
    * EVALUATION: Ask the user how they are feeling now and store the information.
    * WRAPUP: Say goodbye.

* Come up with a list of interventions to try out; allow user to add their own interventions too
* How can we figure out presentation? Can we find an optimal presentation too?
    * Can we auto-generate cute graphics to send to the user?

### Done:
* Research different types of implementations
* Set up Twilio app: https://www.twilio.com/docs/studio/tutorials/how-to-build-a-chatbot

## Idea

Build a text-based chat-bot that prompts the user to track their mental health daily, and walks them through different prevention-based mental health interventions. Will check which interventions work best over time (HabitLab style).

## Goals

1. Give user data back to the user - wrap it up into something pretty
2. Make it super easy and desirable to use and respond to
3. Allow user flexibility to suggest their own interventions and monitor their own behavior

## Details / Notes

### Chatbox personality
* Friendly but professional