<div align='center'>
  <br />
  <p>
    <a href='https://github.com/ThisIsMatin/Yaplee'><img src='https://github.com/ThisIsMatin/Yaplee/blob/main/images/logo.png?raw=true' width='546' alt='Yaplee Logo' /></a>
  </p>
    <br />
  <p>
    <img src='https://img.shields.io/badge/License-MIT-blue' alt='' />  <img src='https://img.shields.io/badge/Testing-passing-green?logo=github' alt='' /> <img src='https://img.shields.io/badge/Python-> 3.6-red?logo=python' alt='' /> 

  </p>
  <h1>Getting Started</h1>
  <h4>Yaplee is a fun and simple python framework to build user interfaces</h4>

</div>

Using Yaplee, you can easily create user interfaces in Python and even use them in your projects.
Here we want to start and create a simple project with Yaplee, all we have to do is use the basic form:
```python
from yaplee import app

myapp = app()

@myapp.init
def Initial():
    myapp.config(debug=True)

myapp.start()
```
First we need to create an application. This application starts by defining `app()` in a variable that we can define the name of anything and then use it. Each yaplee application needs to define the `initial` operation for it, otherwise the project will not run and will encounter an error. In the initial function you can set the project configurations and settings. Each yaplee project starts by calling the `app.start()` function, which only works during debugging, and in sync with different web frameworks for backing up, this operation does not run.

If we do not define any page to display to the user in yaplee, the default page is *Hello, Yaplee!* The user is shown that by running this simple program, you can view this page.

* [Read more document (templates)](https://github.com/ThisIsMatin/Yaplee/blob/main/docs/templates.md)