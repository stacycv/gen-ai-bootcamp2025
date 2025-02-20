# Frontend Technical Specs

## Pages

### Dashboard `/dashboard`

#### Purpose
The purpose of this page is to provide a summary of learning and act as a default page when the user visits the portal.

#### Components
- Last Study Session
    - Shows last activity used
    - Shows when last activity date and time
    - Summarized correct vs incorrect answers from last activity
    - Has link to the group
- Study Progress
    - Total words studied eg. 10/193
        - across all study session show the total words studied out ofall possible words in our database
    - Display a mastery progress eg. 50%
- Quick Stats
    - Success rate eg. 70%
    - Total study sessions eg. 10
    - Total active groups eg. 3
    - Study streak eg. 4 days
- Start Studying Button
    - Goes to study session activites page

#### Needed API Endpoints

- GET /api/dashboard/last-study-session
- GET /api/dashboard/study-progress
- GET /api/dashboard/quick-stats

### Study  Activities `/study-activities`   

#### Purpose    
The purpose of this page is to provide a collection of study activities for the user with a thumbnail and its name, to either launch the activity or view the details.

#### Components
- Study Activity Card
    - Shows a thumbnail of the activity
    - Shows the name of the activity
    - Shows the description of the activity
    - Has a launch button that launches the activity
    - Has a details button that shows the details of past study sessions for this study activity 

#### Needed API Endpoints
- GET /api/study-activities

### Study Activity Show `/study-activities/:id`

#### Purpose
The purpose of this page is to provide a detailed view of a specific study activity with a list of past study sessions and their details.

#### Components
- Study Activity Details
    - Shows the name of the activity
    - Shows the description of the activity
    - Shows the thumbnail of the 
    - Launch Button
    - Study Activties Paginated List
        - id
        - activity name
        - activity description
        - group  name
        - start time
        - end time (infer by the last word review item submitted)
        - number of words reviewed
        - success rate

#### Needed API Endpoints
- GET /api/study-activities/:id
- GET /api/study-activities/:id/study-sessions  

### Study Activities Launch Page `/study-activities/:id/launch`

#### Purpose
The purpose of this page is to launch the study activity and start the study session.

#### Components
- Name of the activity
- Launch form
    - Select filed for group
    - Launch now button

## Behavior
After the form is submitted, a new tab opens with the study activity based on its URL provided in the database.

Also the after the form is submitted, the form page will redirect to the study session show page

#### Needed API Endpoints
- POST /api/study-activities/

### Words Index `/words`

#### Purpose
The purpose of this page is to  show all words in the database.

#### Components
- Words Paginated List
    - Fields
        - Columns
            - Formal Spanish
            - Informal Spanish
            - English
            - Correct Count
            - Wrong Count
        - Pagination with 100 items per page
        - Clicking the Spanish word will open a modal with the word in the informal and formal form

### Needed API Endpoints
- GET /api/words

### Word Show `/words/:id`

#### Purpose
The purpose of this page is to show the details of a specific word.

#### Components
- Formal Spanish
- Informal Spanish
- English
- Study Statistics
    - Correct Count
    - Wrong Count
- Word Groups
    - show a series of pills eg. tags
    - when group name is clicked, it will open a modal with the group details

#### Needed API Endpoints
- GET /api/words/:id

### Word Groups Index `/groups`

#### Purpose
The purpose of this page is to show a list of groups in the database.

#### Components
- Groups Paginated List
    - Columns
        - Group Name
        - Word Count
    - Clickingthe group name will take us to the group show page

#### Needed API Endpoints
- GET /api/groups


### Group Show `/groups/:id`

#### Purpose
The purpose of this page is to show the details of a specific group.

#### Components
- Group Name
- Group Statistics
    - Total Word Count
-Words in Group (Paginated List of Words)
    - Should use the same components as the words index page
- Study Sessions (Paginated List of Study Sessions)
    - Should use the same components as the study sessions index page

#### Needed API Endpoints
- GET /api/groups/:id (the name and group stats)
- GET /api/groups/:id/words
- GET /api/groups/:id/study-sessions

## Study Sessions Index `/study-sessions`

#### Purpose
The purpose of this page is to show a list of study sessions in the database.

#### Components
- Study Sessions Paginated List
    - Columns
        - Id
        - Activity Name
        - Group Name
        - Start Time
        - End Time
        - Number of Review Items
    - Clicking the study session id will take us to the study session show page

#### Needed API Endpoints
- GET /api/study-sessions

### Study Session Show `/study-sessions/:id`

#### Purpose
The purpose of this page is to show the details of a specific study session.

#### Components
- Study Session Details
    - Activity Name
    - Group Name
    - Start Time
    - End Time
    - Number of Review Items
- Word Review Items (Paginated List of Words)
    - Should use the same components as the words index page

#### Needed API Endpoints
- GET /api/study-sessions/:id
- GET /api/study-sessions/:id/words

#### Settings Page `/settings`

#### Purpose
The purpose of this page is to makeconfigurations to the study portal.

#### Components
- Theme Selection eg. light and dark mode
- Reset History Button
    - This will delete all study sessions and word review items
- Full Reset Button 
    - This will drop all tables and recreate with seed data

#### Needed API Endpoints
- POST /api/reset-history
- POST /api/full-reset






