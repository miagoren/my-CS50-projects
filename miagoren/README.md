# WebAid

## Contents

1. [ Description ](#desc)
2. [ Users in WebAid ](#user)
3. [ Messaging on WebAid ](#messaging)
4. [ Opportunities ](#opportunities)
5. [ Managing your opportunities ](#manage)
6. [ Leading helpers ](#helpers)
7. [ Search ](#search)
8. [ Models ](#models)
9. [ Complexity ](#complex)

<a name="desc"></a>
## Description

WebAid is a website that allows any person to get help from other users of the website. Once a user is logged in, they can post new opportunities or volunteer to help other users with their opportunities. I decided to create this web application because at a time like this we can all use help and I was hoping to make it a simple and rewarding process.

<a name="user"></a>
## Users in WebAid

Every user has to fill some additional information about themselves when they first create their account - their location and their skills. All of the information about a certain user is available on their profile page, where you can also view all of the opportunities the user posted and the opportunities they helped resolve. If a user goes to their own profile page, they can edit the information about themselves.

<a name="messaging"></a>
## Messaging on WebAid

To allow users to communicate with one another, there is the messaging system. On the messaging page any authenticated user can view all of their conversations, send messages, or start new conversations. On a user's profile page there is a button that allows any authenticated user to start a new conversation with that user. On the opportunity page there is a button that lets users volunteer for this opportunity by creating a new conversation with the opportunity's creator.

<a name="opportunities"></a>
## Opportunities

Every active opportunity (an opportunity that wasn't resolved) can be viewed on the opportunities page. This page displays all the opportunities, 10 on each page, and lets the user filter them to find the right opportunity for them. The filters available are filtering by categories, by location, and by creation time. Any person can save the filters they applied as their default filters so that every time they visit the page the opportunities they see will be the most relevant ones.

<a name="manage"></a>
## Managing your opportunities

Every authenticated user can create new opportunities by filling in all the necessary information. Their opportunities will be displayed on their profile page. When a user visits the page of their own opportunity, they can edit this opportunity or resolve it. Resolved opportunities still exist on the website but they will not show on the opportunities' page or on the creator's profile. When the creator marks the opportunity as resolved they can give credit to the users that helped them and write a short summary of the experience they had. The resolved opportunity and the summary will appear on the profile page of every user that helped.

<a name="helpers"></a>
## Leading helpers

WebAid presents all of the users that helped most on the home page, a full list of all the leading helpers is also available.

<a name="search"></a>
## Search

On the navigation panel there is a search bar that lets users search for any user or opportunity. In the search results there are resolved opportunities as well as active ones.

<a name="models"></a>
## Models

There are five models in WebAid - User, Opportunity, Conversation, Message, and Resolve.

### User

The User model has two additional fields - location and skills. It also has two built in methods - get_latest_created and get_latest_resolved. The User model helps keep track of every user's activity on WebAid.

### Opportunity

The Opportunity model stores all of the information about the opportunities on WebAid. In addition to the opportunity's data, it keeps track of the creator, creation time and whether the opportunity was resolved. The Opportunity model has two built in methods - get_latest and make_time_difference. The make_time_difference replaces the opportunity's creation_time field with a string that specifies how long ago the opportunity was created.

```
Now: 12:54
Opportunity creation_time: 12:42

New creation_time: 12 minutes ago
```

### Conversation

The Conversation model stores all of the existing conversations. It keeps track of the conversation subject and the users participating in the conversation.

### Message

The Message model keeps track of all of the messages - message body, sender, conversation, and time of creation.

### Resolve

The Resolve model is related to the resolved field of each opportunity. It stores the summary of that opportunity and the users that helped resolve it.

<a name="complex"></a>
## Complexity

WebAid has many elements from the CS50's web programming course. The website is designed using one layout, bootstrap's styling, and Sass. The website uses Django for the backend and JavaScript for frontend.

There are several APIs on WebAid. The opportunity API is for retrieving the latest opportunities without reloading the page. The messaging API deals with displaying conversations and messages, sending messages, and leaving conversations. The helpers API returns the leading helpers, 10 on every page.

The site utilizes Django's forms - New Opportunity Form, New Conversation Form, and Resolve Opportunity Form.

## Author

* Mia Goren
