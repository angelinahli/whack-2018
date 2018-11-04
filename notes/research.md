Questions to answer:
1) How would we implement a project like this?
2) Does this sound feasible given the time we have?

* Chrome extension - Angie
    - Extensions are zipped bundles of HTML, CSS, JS, images, etc.
    - https://robots.thoughtbot.com/how-to-make-a-chrome-extension
    - Doesn't seem SUPER hard to at least start making a chrome extension like I think we can do it.

* Facebook based messenger app? - Angie
    * https://developers.facebook.com/docs/messenger-platform/getting-started/quick-start/#getting_started

Here are some ideas for grounding activities:

-Take deep, calm breaths.
-Notice and list things in your surroundings.
-Expose yourself to strong, pleasant sensations, like a pleasing smell or a favorite blanket.
-Say out loud your name, your age, the date, and your location. List some things you've done today, or are going to do.
-Splash water on your face or run your hands under the faucet.
-Do a body scan meditation, or pay close attention to each of your body parts one by one.
-Make tea. Feel the warmth of it in your hands, and the taste as you sip it calmly.
-Listen to music.
-Play a categories game, and name some types of dogs, or clothing items, or gemstones, or countries, or anything else you can think of.
-Write in your journal.
-Take a mindful walk, either inside or outside. Pay close attention to your body and your surroundings.
-Squiggle. Wiggle around. Dance. Stretch. Be silly and active for a few minutes.
-Any other favorite grounding technique you've heard of or can think of. There's nothing wrong with experimenting!



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
