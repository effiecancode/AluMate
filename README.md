# ELP portal

## Description

-   A student portal to consolidate ELP and Wings To Fly alumni data, manage opportunities and events invitations.

## Backend

### Technologies

The project is created with:

-   Python Django
-   Django RestFramework
-   drf_yasg(swagger) -- for endpoint documentation

### Installation

-   Make sure Python is installed.

```text
python 3.8.10
```

-   Clone https://github.com/ElpTechHub/techhub-portal-backend.git and cd into techhub-portal-backend.

-   Install requirements using following command.

```text
To install requirements run:
make requirements or python3 manage.py install -r requirements.txt || pipenv install --dev
```

### Environment Variables

| Variable                             | Description                                                                                                                                                                                    | Default                |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| <sup>**SECRET_KEY**</sup>            | <sup>**Required** - String of random characters used to provide cryptographic signing for [Django](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-SECRET_KEY) projects.</sup> | <sup></sup>            |
| <sup>**DB_NAME**</sup>               | <sup>**Required** - Used to represent the name of the database</sup>                                                                                                                           | <sup></sup>            |
| <sup>**ENVIRONMENT**</sup>           | <sup> **Optional** - Used to load different settings according to the environment selected. Choices: `production`, `development`, `common`</sup>                                               | <sup>development</sup> |
| <sup>**DB_USER**</sup>               | <sup> **Required** - Used to represent username </sup>                                                                                                                                         | <sup></sup>            |
| <sup>**DB_PASSWORD**</sup>           | <sup> **Required** - database password</sup>                                                                                                                                                   | <sup></sup>            |
| <sup>**DB_HOST**</sup>               | <sup> **Required** - Database host</sup>                                                                                                                                                       | <sup></sup>            |
| <sup>**CLOUDINARY_CLOUD_NAME**</sup> | <sup> **Required** - required by [https://cloudinary.com](https://cloudinary.com) to identify the cloud name</sup>                                                                             | <sup></sup>            |
| <sup>**CLOUDINARY_API_KEY**</sup>    | <sup> **Required** - provided by [https://cloudinary.com](https://cloudinary.com) to uniquely identify the client </sup>                                                                       | <sup></sup>            |
| <sup>**CLOUDINARY_API_SECRET**</sup> | <sup> **Required** - provided by [https://cloudinary.com](https://cloudinary.com) to authenticate in conjuction with the CLOUDINARY_API_KEY </sup>                                             | <sup></sup>            |

### Usage

-   Clone the repository:\
    a. Using SSH:

    ```text
    git clone git@github.com:ElpTechHub/techhub-portal-backend.git
    ```

    b. Using Http:

    ```tet
    git clone https://github.com/ElpTechHub/techhub-portal-backend.git
    ```

-   Navigate to the cloned folder:

    ```text
    cd techhub-portal-backend
    ```
-   Pre-commit hook

    ```text
    pre-commit install
    ```


-   Create a virtual environment.

```text
python3 -m venv venv

Or Install virtualenv then
virtualenv venv

On Linux ~ source venv/bin/activate

On windows ~ venv\Scripts\Activate

Or run pipenv shell
```

-   Configuring postgres Ubuntu

```text
Update: sudo apt update
Installing: sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib
First login by running: sudo -u postgres psql
Create DB: CREATE DATABASE elpportal;
Create USER: CREATE USER elpportaldev WITH PASSWORD 'elpportaldev@';
run: \q to exit server
```

-   Run migrations.

```text
make migrations ~ python manage.py makemigrations

make migrate ~ python manage.py migrate
```

-   Create a super user.

```text
python manage.py createsuperuser
```

-   Run the app.

```text
make serve ~ python manage.py runserver
```

-   This opens the app at {{BASE_URL}}

```text
localhost:8000
```

or

```text
http://127.0.0.1:8000/

```

### Endpoints Implemented

-   Events: "{{BASE_URL}}/api/events/",
-   Hubs: "{{BASE_URL}}/api/hubs/"
-   Chapters: "{{BASE_URL}}/api/chapters/"
-   Opportunities: "{{BASE_URL}}/api/opportunities/"
-   Auth: "{{BASE_URL}}/api/user/sign-in/"
    "{{BASE_URL}}/api/user/register/ "

### Chapter Endpoints
```
- Create Chapter[POST]: {{BASE_URL}}/api/chapters/
- Get a List of Chapters[GET]: {{BASE_URL}}/api/chapters/
- Update Chapter[PUT]: {{BASE_URL}}/api/chapters/{chapter_id}/update_chapter/
- Delete Chapter[DELETE]: {{BASE_URL}}/api/chapters/{chapter_id}/delete_chapter/
- Search Chapter by Name [GET]: {{BASE_URL}}/api/chapters/search-chapter{chapter_name}/
- Search Chapters by ID [GET]: {{BASE_URL}}/api/chapters/{chapter_id}/
- Register User [POST]: {{BASE_URL}}/api/chapters/<chapter_id>/register/

```


**_DEVELOPERS_**
- Tech Hub Team