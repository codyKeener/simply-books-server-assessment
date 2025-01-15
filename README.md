# Welcome to the Simply Books Django server assessment!

This project was completed in a 1 week sprint of 6 days as an assessment of my understanding of setting up a back end server in Django and Python.

## Get Started

Please see the [API Documentation](https://documenter.getpostman.com/view/35026527/2sAYQXnYBH)

## About the User
- The ideal user for this application is anyone who wants to create, read, update, and delete books
- They want to see books they have added to their library as well as information about the authors of those books
- The problem this app solves for them is that it allows users to keep track of all of their books and authors

## Features
- Create, Read, Update, and Delete authors
- Create, Read, Update, and Delete books
- Create, Read, Update, and Delete genres
- Create, Read, Update, and Delete bookGenres (many-to-many relationship between books and genres)

## Video Walkthrough of Simply Books Django server assessment
[Loom Video Walkthrough](https://www.loom.com/share/b3c335e20467441a902e0d0a2ef0e134?sid=b77edf9f-13d7-4f65-bdaf-381ff2e2695a)

## Relevant Links
- Please see the [API Documentation](https://documenter.getpostman.com/view/35026527/2sAYQXnYBH)
- Check out this [Loom Video](https://www.loom.com/share/13ed4c65e103473f818680ae655ca27b?sid=c38638c5-47bd-4738-b3a9-a0f4a36e2cf4) for a demonstration of some of the endpoints in Postman

## Code Snippet

<!-- // Author Model -->

```
class Author(models.Model):
  
  email = models.CharField(max_length=50)
  first_name = models.CharField(max_length=30)
  last_name = models.CharField(max_length=30)
  image = models.URLField()
  favorite = models.BooleanField()
  uid = models.CharField(max_length=30)
```

## Contributors
- Cody Keener (https://github.com/codyKeener)

## ------------------------------------------------------------------------------------------ ##

## Instructions I followed

- [Simply Books API-Back End RUBRIC](https://docs.google.com/spreadsheets/d/1Ijb2Z6kY-2s4KmTdAwoMiKZ_CFj_FodfEOvrd3K70yc/edit?usp=sharing)

- [BACK END: Definition of Done](#be-definition-of-done)
- [MVP Guidelines](#mvp-guidelines)
- [Guide to getting started with this project](#guide-to-getting-started)

### BE Definition of Done
A feature or task is considered "done" when:
1. All tasks, features, and fixes must be ticketed and included on the GitHub project board.
Make sure the project board uses columns like Backlog, In Progress, Testing, and Done to track work.
1. The code is fully implemented and meets the requirements defined in the task.
1. The feature passes all AC especially for CRUD functionality.
1. The user can successfully perform Create, Read, Update, and Delete operations for both books and authors using postman.
1. All relationships between authors and books are correctly established and maintained.
1. The API docs are deployed on Postman, and all features work in the deployed environment.
1. The README is updated with any relevant instructions, and a Loom video (max 5 minutes) demonstrates the app's features.
1. For any stretch goals, the feature must be functional and demonstrate proper user interaction (e.g., public/private book functionality, simulated purchase).
1. Any issues or bugs identified during development or testing must be fixed by the developer. All work related to fixes must be ticketed and included on the GitHub project board.
1. The project board must reflect all tasks, bugs, and updates, with each task being moved through the proper columns (Backlog, In Progress, Testing, Done).

### MVP Guidelines
The Minimum Viable Product (MVP) for the Simply Books project includes:
1. **CRUD Functionality for Books and Authors**:
   - Users must be able to create, read, update, and delete books and authors.
   - When viewing an author, all books associated with that author must be visible.
   - When deleting an author, all of their books are also deleted.
   
2. **Author-Book Relationship**:
   - Each book must be associated with an author.
   - When a user views a book, the associated author's details must be accessible.
   
3. **Firebase Integration**:
   - The app must use Firebase for authentication and real-time data management.
   - Books and authors are tied to the logged-in user.

4. **User-Specific Data**:
   - Each user should only see their own books and authors.

#### Stretch Goals:
- **Public/Private Books**:
   - Users can mark books as public or private.
   - Public books are viewable by all users without needing to log in.
   - Private books are only visible to the user who created them.
   
- **Simulated Book Purchases**:
   - Users can add books to a cart and simulate purchasing them.
   - No real transaction will occur, but the UI will allow users to add items to the cart and check out.

### Guide to Getting Started
Follow the deployment guide to get your app live!

1. **Follow the Guide**:
   - Detailed steps for each part of the project can be found in the [Guide to getting started with this project](/project-docs/GET_STARTED.md).

1. **Submit**:
   - Make sure to complete the README, Loom video demonstration, and submit your project with the deployed link.
