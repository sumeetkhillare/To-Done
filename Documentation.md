# Django Todo Application Views Documentation

This document provides an overview of the views in the Django Todo application, including their purpose, parameters, and expected outcomes.

## Table of Contents
- [Overview](#overview)
- [Views](#views)
  - [Index View](#index-view)
  - [Create Todo from Template](#create-todo-from-template)
  - [Create Template from Todo](#create-template-from-todo)
  - [Delete Todo](#delete-todo)
  - [Template View](#template-view)
  - [Remove List Item](#remove-list-item)
  - [Update List Item](#update-list-item)
  - [Add New List Item](#add-new-list-item)
  - [Mark List Item](#mark-list-item)
  - [Get List Tags by User ID](#get-list-tags-by-user-id)
  - [Get List Item by Name](#get-list-item-by-name)
  - [Get List Item by ID](#get-list-item-by-id)
  - [Create New Todo List](#create-new-todo-list)
  - [User Registration](#user-registration)
  - [User Login](#user-login)
  - [User Logout](#user-logout)
  - [Password Reset Request](#password-reset-request)
  - [Google Auth Receiver](#google-auth-receiver)
  - [Kanban View](#kanban-view)
  - [Add Task](#add-task)
  - [Update Task](#update-task)
  - [Delete Task](#delete-task)
  - [Update Task Status](#update-task-status)

## Overview
The Todo application allows users to manage tasks through a visual interface. Users can create, update, delete, and share tasks and lists. The application incorporates user authentication and authorization.

## Views

### Index View
- **URL:** `/`
- **Method:** `GET`
- **Description:** Renders the homepage displaying the user's to-do lists.
- **Parameters:**
  - `list_id` (int, optional): ID of a specific list to display.
- **Response:**
  - Status Code: `200`
  - Template Used: `todo/index.html`
  - Context: Includes latest lists, items, templates, and shared lists.

### Create Todo from Template
- **URL:** `/todo/from-template/`
- **Method:** `POST`
- **Description:** Creates a new todo list from a selected template.
- **Parameters:**
  - `template` (int): ID of the template to use.
- **Response:**
  - Redirects to the todo list homepage.

### Create Template from Todo
- **URL:** `/template/from-todo/`
- **Method:** `POST`
- **Description:** Creates a new template from an existing todo list.
- **Parameters:**
  - `todo` (int): ID of the todo list.
- **Response:**
  - Redirects to the templates list page.

### Delete Todo
- **URL:** `/todo/delete/`
- **Method:** `POST`
- **Description:** Deletes a specified todo list.
- **Parameters:**
  - `todo` (int): ID of the todo list to delete.
- **Response:**
  - Redirects to the todo list homepage.

### Template View
- **URL:** `/templates/`
- **Method:** `GET`
- **Description:** Renders the page displaying the user's templates.
- **Parameters:**
  - `template_id` (int, optional): ID of a specific template to display.
- **Response:**
  - Status Code: `200`
  - Template Used: `todo/template.html`
  - Context: Includes the user's templates.

### Remove List Item
- **URL:** `/list-item/remove/`
- **Method:** `POST`
- **Description:** Removes a specified list item.
- **Parameters:**
  - `list_item_id` (int): ID of the list item to remove.
- **Response:**
  - Redirects to the todo list homepage.

### Update List Item
- **URL:** `/list-item/update/<int:item_id>/`
- **Method:** `POST`
- **Description:** Updates the text of a specified list item.
- **Parameters:**
  - `item_id` (int): ID of the list item to update.
  - `note` (string): New text for the list item.
- **Response:**
  - Redirects to the homepage.

### Add New List Item
- **URL:** `/list-item/add/`
- **Method:** `POST`
- **Description:** Adds a new item to a specified list.
- **Parameters:**
  - `list_id` (int): ID of the list.
  - `list_item_name` (string): Name of the new list item.
  - `create_on` (timestamp): Creation time.
  - `due_date` (timestamp): Due date for the item.
  - `tag_color` (string): Color associated with the item.
- **Response:**
  - JSON Response: Contains the ID of the newly created item.

### Mark List Item
- **URL:** `/list-item/mark/`
- **Method:** `POST`
- **Description:** Marks a list item as done or not done.
- **Parameters:**
  - `list_id` (int): ID of the list.
  - `list_item_id` (int): ID of the list item.
  - `is_done` (bool): Status to set (done or not done).
- **Response:**
  - JSON Response: Includes the item name and list name.

### Get List Tags by User ID
- **URL:** `/list-tags/`
- **Method:** `POST`
- **Description:** Retrieves all list tags associated with the authenticated user.
- **Parameters:** None
- **Response:**
  - JSON Response: List of tags.

### Get List Item by Name
- **URL:** `/list-item/name/`
- **Method:** `POST`
- **Description:** Retrieves a specific list item by name.
- **Parameters:**
  - `list_id` (int): ID of the list.
  - `list_item_name` (string): Name of the list item.
- **Response:**
  - JSON Response: Contains details of the found item.

### Get List Item by ID
- **URL:** `/list-item/id/`
- **Method:** `POST`
- **Description:** Retrieves a specific list item by ID.
- **Parameters:**
  - `list_id` (int): ID of the list.
  - `list_item_id` (int): ID of the list item.
- **Response:**
  - JSON Response: Contains details of the found item.

### Create New Todo List
- **URL:** `/todo/create/`
- **Method:** `POST`
- **Description:** Creates a new todo list.
- **Parameters:**
  - `list_name` (string): Name of the new list.
  - `create_on` (timestamp): Creation time.
  - `list_tag` (string): Associated tag for the list.
  - `shared_user` (string): User(s) to share the list with.
- **Response:**
  - JSON Response: Success message.

### User Registration
- **URL:** `/register/`
- **Method:** `POST`
- **Description:** Registers a new user account.
- **Parameters:**
  - Form data for user registration.
- **Response:**
  - Redirects to the todo index on success or re-renders the registration form with errors.

### User Login
- **URL:** `/login/`
- **Method:** `POST`
- **Description:** Authenticates a user and logs them in.
- **Parameters:**
  - Form data for authentication (username and password).
- **Response:**
  - Redirects to the todo index on success or re-renders the login form with errors.

### User Logout
- **URL:** `/logout/`
- **Method:** `GET`
- **Description:** Logs out the authenticated user.
- **Parameters:** None
- **Response:**
  - Redirects to the todo index.

### Password Reset Request
- **URL:** `/password_reset/`
- **Method:** `POST`
- **Description:** Initiates a password reset for a user.
- **Parameters:**
  - Email address of the user requesting the reset.
- **Response:**
  - Redirects to a confirmation page on success.

### Google Auth Receiver
- **URL:** `/auth/receiver/`
- **Method:** `POST`
- **Description:** Receives Google authentication tokens and logs in the user.
- **Parameters:**
  - `credential` (string): Google authentication token.
- **Response:**
  - Redirects to the login page.

### Kanban View
- **URL:** `/kanban/`
- **Method:** `GET`
- **Description:** Renders the Kanban view displaying the user's tasks.
- **Parameters:** None
- **Response:**
  - Status Code: `200`
  - Template Used: `todo/kanban_dd.html`
  - Context: Contains tasks associated with the user.

### Add Task
- **URL:** `/task/add/`
- **Method:** `POST`
- **Description:** Adds a new task for the authenticated user.
- **Parameters:**
  - `title` (string): Title of the new task.
- **Response:**
  - JSON Response: Success message.

### Update Task
- **URL:** `/task/update/<int:task_id>/`
- **Method:** `POST`
- **Description:** Updates the status of a specified task.
- **Parameters:**
  - `task_id
