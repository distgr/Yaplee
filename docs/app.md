<div align='center'>
  <br />
  <p>
    <a href='https://github.com/ThisIsMatin/Yaplee'><img src='https://github.com/ThisIsMatin/Yaplee/blob/main/images/logo.png?raw=true' width='546' alt='Yaplee Logo' /></a>
  </p>
    <br />
  <p>
    <img src='https://img.shields.io/badge/License-MIT-blue' alt='' />  <img src='https://img.shields.io/badge/Testing-passing-green?logo=github' alt='' /> <img src='https://img.shields.io/badge/Python-> 3.6-red?logo=python' alt='' /> 

  </p>
  <h1>App object</h1>
  <h4>Yaplee is a fun and simple python framework to build user interfaces</h4>

</div>

<details open>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#">App object</a></li>
    <li><a href="#add-initial-decorator">Initial decorator</a></li>
    <li><a href="#config">Config</a></li>
    <li><a href="#global-validators">Global validators</a></li>
  </ol>
</details>

# App object
Each yaplee file consists of an app object that manages the entire project using this object. The existence of this object is essential for the implementation and continuation of the project.

## Add initial decorator
A yaplee project always has an initial function, otherwise the project will not run. In this function you can enter the commands and settings that you want to execute when starting the project. An example of this function is as follows:

```python
@myapp.init
def Initial():
    pass
```

## Config
The app object has a function called config that you can use to make project-related settings in the simplest way. This command can only be executed in the initial function of the project. Just enter the setting name along with the value you want to this function, for example we can turn on the project debug mode:
```python
@myapp.init
def Initial():
    myapp.config(debug=True)
```
Here is a list of configurable settings:
* `debug` -> bool : To set the project debug mode which is **True** by default. This setting should be turned off when syncing with web frameworks.
* `port` -> int : Development server port
* `sync` -> str : To determine to sync with web frameworks (input is the name of the web framework, for example **django**)
* `opentab` -> bool : To open the Development Server tab (if True, the Development Server URL will automatically open in your browser when you run the project)

## Global validators
Using global variables you can access general variables in the project.

* Config global variables :
  * `is_debug` -> bool : Debug mode status in config
  * `opentab` -> bool : Automatic open local project tab in browser
  