<div align='center'>
  <br />
  <p>
    <a href='https://github.com/ThisIsMatin/Yaplee'><img src='https://github.com/ThisIsMatin/Yaplee/blob/main/images/logo.png?raw=true' width='546' alt='Yaplee Logo' /></a>
  </p>
    <br />
  <p>
    <img src='https://img.shields.io/badge/License-MIT-blue' alt='' />  <img src='https://img.shields.io/badge/Testing-passing-green?logo=github' alt='' /> <img src='https://img.shields.io/badge/Python-> 3.6-red?logo=python' alt='' /> 

  </p>
  <h1>Sync with other web frameworks</h1>
  <h4>Yaplee is a fun and simple python framework to build user interfaces</h4>

</div>

<details open>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#introduction">Introduction</a></li>
    <li>
      <a href="#">Sync yaplee project with...</a>
      <ul>
        <li><a href="#sync-with-django">Django</a></li>
      </ul>
    </li>
  </ol>
</details>

## Introduction
The Yaplee framework can be synced with other web frameworks, and you can use Yaplee-created pages in other web frameworks. Yaplee has the ability to sync automatically and in just a few seconds you can sync your project with other frameworks

## Sync with Django
#### Automatic Sync :
To create an Yaplee project and sync it automatically with your Django project, first go to the main folder of your Django project (where manage.py is located) :

```bash
$ sudo django-admin startproject testproject
$ cd testproject/
```
Then create an Yaplee app here and set the sync argument to Django:
```bash
$ sudo yaplee new --sync django
```
Done! Your Django project is now synced with the Yaplee app.
### How it works ?
1. Create an Yaplee template first:
    ```python
    @myapp.template('main.html')
    def MainPage():
        return {}
    ```
    Note: Create a `main.html` file in django main folder (It is recommended to put the HTML files in a folder and organize the project).
2. Create a view in Django:
    ```python
    def home(request):
        return render(request, 'main.html')
    ```
    Then set this view (for example) to the project's main page:
    ```python
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', home)
    ]
    ```
3. Done! Now start your Django project:
    ```bash
    $ sudo python3 manage.py runserver

    [Yaplee] : Preparing your application...
    Watching for file changes with StatReloader
    Performing system checks...

    System check identified no issues (0 silenced).
    Django version *, using settings 'testproject.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.
    ```