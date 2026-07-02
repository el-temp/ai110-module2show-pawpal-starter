# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

There will be four classes; Owner, Pet, Task, and Sceduler. Owner and Pet will contain basic information about their respective things, while task and design will 

- What classes did you include, and what responsibilities did you assign to each?

Owner attributes: name, address, pets
Owner methods: edit_name, edit_address, add_pet, remove_pet, edit pet
Pet attributes: pet_name, pet_type, special notes
Pet methods: add_info, delete_info, edit_info
Task attributes: description, due_time, completion_status
Task Methods: edit description, edit due_time, mark_complete
Scheduler: organize tasks by due date, filter by pet

**b. Design changes**

- Did your design change during implementation?
Yes
- If yes, describe at least one change and why you made it.
One change it made was importing pythons built in time object. The original implementation put time as a String which would cause some problems during sorting which should in theory be fixed now that it uses time object

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
The constraint that the system makes is the time and prirotity. 
- How did you decide which constraints mattered most?
Preferences is left pretty open for editing but making sure the timing of task is correct is integral.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
For my filter_by_pet method there was a suggestion to reduce the time complexity by adding a dictionary however that was not implemented into this code. Instead it was left largely as is to help with readability.
- Why is that tradeoff reasonable for this scenario?
This tradeoff is reasonable since overall the prohject is not very resource intensive so being able to understand the code for a small loss of effieceny is a worthwhile trade.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
