# Blogging App

## Description

A simple blogging platform built with **Django** and **Django REST Framework** that allows users to:
- Register & authenticate using JWT tokens  
- Create, edit, delete, and browse blog posts  
- Follow/unfollow other users and see their posts

## 📦 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/Mustafa-Yusa-Babademez/blogging.git
cd blogging
```
### 2. Create and activate a virtual environment
(Unix / macOS)
```bash
python -m venv venv
source venv/bin/activate
```
(Windows)
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### Run migrations and start server
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser   # optional: create admin
python manage.py runserver
```


## 📌 API Endpoints

---

### Authentication & User

#### 1. Register User  
**POST** `/api/register/`  
Registers a new user.

**Raw JSON body**
```json
{
  "username": "yusa",
  "email": "yusa@yusa.com",
  "password": "password123"
}
```

#### 2. Login (Obtain Token)
**POST** `/api/token/`
Returns access and refresh tokens.

**Raw JSON body**
```json
{
  "username": "yusa",
  "password": "password123"
}
```
### Post
#### 1. Create a post  
**POST** `/api/posts/`

**Raw JSON body**
```json
{
  "title": "My First Blog",
  "content": "This is the content of my first post."
}
```

#### 2. Update a Post
**PUT** `/api/posts/{id}/`

**Raw JSON body**
```json
{
  "title": "Updated Title",
  "content": "Edited content"
}
```

#### 3. See All Posts (global feed)
**GET** `/api/posts/`

#### 4. See My Posts
**GET** `/api/posts/mine/`

#### 5. Delete My Post
**DELETE** `/api/posts/<id>/`

#### 6. See Followings' Posts (friends feed)
**GET** `/api/posts/friends/`

### Follow

#### 1. Follow a user
**POST** `/api/follow/`

**Raw JSON body**
```json
{
  "username": "mustafa"
}
```

#### 2. Unfollow a user
**POST** `/api/follow/unfollow/`

**Raw JSON body**
```json
{
  "username": "mustafa"
}
```

#### 3. List Who I Follow (Following List)
**GET** `/api/follow/following/`

#### 4. List My Followers
**GET** `/api/follow/followers/`
