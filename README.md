# NotesAPIs

Problem - Built a secure and scalable RESTful API that allows users to create, read, update, and delete notes. The
application should also allow users to share their notes with other users and search for notes based on keywords

#### PORT - 59004

#### How To Run:
- install all the requirements from the requirements file
- python ServerMain.py
- Using MongoDB for the NOSQL database
- Built using python Flask
- For search functionality to enable users to search for notes based on keywords - used MongoDB indexing and search text functionality
- For rate limiting and request throttling to handle high traffic - Implemented a custom rate limiting function which will allow the user which is defined in the max_calls variable.
- For testing, I used my local MongoDB server but can change mongo authentication/connect details in conf/settings.conf file

## API Endpoints :

- For create a new user account - http://localhost:59004/api/auth/signup  --> [POST REQUEST]
- For log in to an existing user account and receive an access
  token - http://localhost:59004/api/auth/login  --> [POST REQUEST]
- For getting a list of all notes for the authenticated user - http://localhost:59004/api/notes     --> [GET REQUEST]
- For getting a note by ID for the authenticated user - http://localhost:59004/api/notes/:id     --> [GET REQUEST]
- For creating a new note for the authenticated user. - http://localhost:59004/api/notes     --> [POST REQUEST]
- For updating an existing note by ID for the authenticated
  user - http://localhost:59004/api/notes/:id    --> [PUT REQUEST]
- For deleting a note by ID for the authenticated user - http://localhost:59004/api/notes/:id     --> [DELETE REQUEST]
- For sharing a note with another user for the authenticated
  user - http://localhost:59004/api/notes/:id/share     --> [POST REQUEST]
- For searching for notes based on keywords for the authenticated
  user - http://localhost:59004/api/search?q=:query     --> [GET REQUEST]

**SignUP Input JSON : (/api/auth/signup)**

```
{
    "username": "aman007",
    "password": "aman@123",
    "fullname": "Aman Khandelwal",
    "email": "amankhandelwaljuly@gmail.com"
}
```

- While updating the data I'm creating one unique UUID for that particular cart and also storing the timestamp.

**Login JSON :**

![Alt text]()
- In login API I'm passing username and password within the Authorization header
- Maintaining Rate Limiter for the API

**POST api/notes - Add Notes**

```
{
    "title": "Meet Apar",
    "content": "Don't forget to catch up with Apar over the upcoming weekend"
}
```

- Checking the token expiry before executing the functionality
- Maintaining Rate Limiter for the API

**PUT api/notes - Update Notes**

```
{
    "title": "Meet Aman",
}
```

- Checking the token expiry before executing the functionality
- Update the required fields
- Maintaining Rate Limiter for the API

**Share Notes API - api/notes/:id/share:**

```
request : http://localhost:59004/api/notes/notes_collection_8bb433eaedd144229adb69f064f0706f/share
{
    "username": "apar025"
}
```

- Checking the token expiry before executing the functionality
- Share the notes among the provided user
- Maintaining Rate Limiter for the API

[//]: # (### [Reference Video Link]&#40;https://drive.google.com/file/d/1Gv2eGbq7D9DyMBZXjPGGILcpZWWwl1st/view&#41;)

## Code credit

Code credits for this code go to [Aman Khandelwal](https://github.com/wolfblunt)