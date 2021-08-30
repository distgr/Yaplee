<div align='center'>
  <br />
  <p>
    <a href='https://github.com/ThisIsMatin/Yaplee'><img src='https://github.com/ThisIsMatin/Yaplee/blob/main/images/logo.png?raw=true' width='546' alt='Yaplee Logo' /></a>
  </p>
    <br />
  <p>
    <img src='https://img.shields.io/badge/License-MIT-blue' alt='' />  <img src='https://img.shields.io/badge/Testing-passing-green?logo=github' alt='' /> <img src='https://img.shields.io/badge/Python-> 3.6-red?logo=python' alt='' /> 

  </p>
  <h1>Templates</h1>
  <h4>Yaplee is a fun and simple python framework to build user interfaces</h4>

</div>

<details open>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#adding-a-template">Adding a template</a></li>
    <li>
      <a href="#">Add tags to template</a>
      <ul>
        <li><a href="#link-css-files">Link css files</a></li>
        <li><a href="#add-tags-using-tagmanager-recommended">Add tags using TagManager (Recommended)</a></li>
      </ul>
    </li>
  </ol>
</details>

## Adding a template
To define the existence of a page and finally display it to users, you must use the `app.template` decorator. Each template in yaplee must return a dictionary otherwise it will encounter an error.
Example :

* `main.html` (in yaplee file root) :
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hello, Yaplee!</title>
</head>
<body>
    <h1>Hello, Yaplee!</h1>
</body>
</html>
```

* Yaplee file :
```python
from yaplee import app

myapp = app()

@myapp.init
def Initial():
    myapp.config(debug=True)

@myapp.template('main.html')
def MainPage():
    return {}

myapp.start()
```

If you run this project you will still see the default yaplee page (because the *index.html* file is not defined) but you can view or select the defined pages from the yaplee default page.

## Link css files
You can simply link the css files to your template. This method is only for quick work and if you want to do more personalization, it is recommended to use the [manual method](#add-tags-using-tagmanager-recommended).

If you want to link only one file to the template, you can set the `style` value to one sting that receives the file name :
```python
@myapp.template('main.html')
def MainPage():
    return {'style': 'style.css'}
```
If you need to add several styles, you can put a list in `style` so that all the files are linked to your project :
```python
@myapp.template('main.html')
def MainPage():
    return {'style': ['style.css', 'font-awesome.css', ...]}
```

## Add tags using TagManager (Recommended)
You can use TagManager to optimize tags in a yaplee template. (This method is recommended due to high personalization). First you need to import the tags from yaplee.utils:
```python
from yaplee import app
from yaplee.utils import tags

... 
```

Then just create a new object from `tags.TagManager` in your template and enter the name of the tag you want the tags to be in (for example `head`) and then return that object in the tags value :
```python
@myapp.template('main.html')
def MainPage():
    head_tags = tags.TagManager('head')
    return {'tags': head_tags}
```

You can then add the tags you want to TagManager using `.add()` with full customization:
```python
@myapp.template('main.html')
def MainPage():
    head_tags = tags.TagManager('head')

    head_tags.add('link', rel='stylesheet', href='style.css')
    head_tags.add('meta', charset='UTF-8')

    return {'tags': head_tags}
```