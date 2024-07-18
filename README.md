# Django Task 1

- **Description:** Create an application to enable signup and login for different types of users. On login redirect users to their respective dashboards.

## Tasks

1. Two types of users
2. Signup form
3. Check if password and confirm password match
4. Dashboard for each user

```
Details:

1.Types of Users:
  a. Patient
  b. Doctor

2. The signup form should have following fields:
  a. First Name
  b. Last Name
  c. Profile Picture
  d. Username
  e. Email Id
  f. Password
  g. Confirm Password
  h. Address(line1, city, state, pincode)

3. There should be a check to see if the password and confirm password fields match

4. There is no specific structure for the dashboards…….can simply display the details entered in the signup form
```

# Django Task 2


- **Description:** Integrate a blog system within the application created in the previous task. The doctors can upload new blog posts and the patients can view them. 

## Tasks

```
Details:

1. Create any 4 categories eg. Mental Health, Heart Disease, Covid19, Immunization etc. 
2. Allow the doctor user to create new blog posts. The upload form should have the following fields:
   - Title
   - Image
   - Category
   - Summary
   - Content
3. The blog writer can mark a blog as a draft, while uploading. 
4. The doctors can see the posts uploaded by them.
5. The patient user should see lists of all the blog posts uploaded and not marked as draft, category wise.
6. Each item in the list should contain 
   - title of the post 
   - image of the post
   - the summary with the world limit to 15. If in case the summary is longer than the given word limit, truncate the summary to 15 words and append ‘...’ at the end.
```

