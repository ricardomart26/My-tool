

## How to install django ##

pip install django
sudo apt-get install python3-django




## Projects vs apps ##

What’s the difference between a project and an app? An app is a web application that does something – e.g., a blog system, a database of public records or a small poll app. A project is a collection of configuration and apps for a particular website. A project can contain multiple apps. An app can be in multiple projects.



## What is a view ## 

In Django, a view is a Python function that takes a web request and returns a web response. The response can be the HTML contents of a web page, or a redirect, or a JSON or XML document, or any other type of content.

Views determine what content is displayed when a user visits a particular URL in your web application. When a user makes a request to a URL, Django's URL dispatcher routes (Software that determines what pending tasks should be done next and assigns the available resources to accomplish it.) the request to the appropriate view function, which then generates the HTTP response that is sent back to the user's browser.

Here's an example of a simple view function that returns a greeting message:

```python
from django.http import HttpResponse

def hello(request):
    return HttpResponse("Hello, world!")
```

This view function takes a request object as its parameter and returns an HttpResponse object that contains the string "Hello, world!". When a user visits the URL that is associated with this view, the function is called and the message is returned in the HTTP response.

You can map this view to a URL in your urls.py file like this:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello, name='hello'),
]
```

This maps the /hello/ URL to the hello view function. When a user visits /hello/, the view function is called and the "Hello, world!" message is returned in the HTTP response.


The next step is to point the root URLconf at the hello.urls module. In mysite/urls.py, add an import for django.urls.include and insert an include() in the urlpatterns list, so you have:

mysite/urls.py

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("hello/", include("hello.urls")),
    path("admin/", admin.site.urls),
]
```

The include() function allows referencing other URLconfs. Whenever Django encounters include(), it chops off whatever part of the URL matched up to that point and sends the remaining string to the included URLconf for further processing.

The idea behind include() is to make it easy to plug-and-play URLs. Since hello are in their own URLconf (hello/urls.py), they can be placed under “/hello/”, or under “/fun_hello/”, or under “/content/hello/”, or any other path root, and the app will still work.

When to use include()

You should always use include() when you include other URL patterns. admin.site.urls is the only exception to this.

You have now wired an index view into the URLconf. Verify it’s working with the following command:

```shell
python manage.py runserver 8000
```

Go to http://localhost:8000/hello/ in your browser, and you should see the text “Hello, world. You’re at the hello index.”, which you defined in the index view.


The path() function is passed four arguments, two required: route and view, and two optional: kwargs, and name. At this point, it’s worth reviewing what these arguments are for.

#### path() argument: route ####

route is a string that contains a URL pattern. When processing a request, Django starts at the first pattern in urlpatterns and makes its way down the list, comparing the requested URL against each pattern until it finds one that matches.

Patterns don’t search GET and POST parameters, or the domain name. For example, in a request to https://www.example.com/myapp/, the URLconf will look for myapp/. In a request to https://www.example.com/myapp/?page=3, the URLconf will also look for myapp/.

#### path() argument: view ####

When Django finds a matching pattern, it calls the specified view function with an HttpRequest object as the first argument and any “captured” values from the route as keyword arguments. We’ll give an example of this in a bit.

#### path() argument: kwargs ####

Arbitrary keyword arguments can be passed in a dictionary to the target view.

#### path() argument: name ####

Naming your URL lets you refer to it unambiguously from elsewhere in Django, especially from within templates. This powerful feature allows you to make global changes to the URL patterns of your project while only touching a single file.




## django models ##

To create a Django model you need to create a class that inherits from models.Model like this:

```python
from Django.db import models

class MyModel(models.Model):
```

### Django models methods ###

1. save() saves the model instance to the database. It can be used to create a new record or update an existing record.
2. delete() deletes the model instance from the database.
3. get_or_create() retrieves an object from the database based on certain criteria, or creates a new object if it does not exist.
4. update() updates one or more fields of an existing record in the database.
5. all() retrieves all objects of the model from the database.
6. filter() retrieves a subset of objects that match a certain criteria.
7. order_by() orders the queryset by one or more fields.
8. annotate() adds extra information to each object in the queryset, based on aggregate functions or other calculations.. 
9. distinct() returns a queryset with distinct results.
10. count() returns the number of objects that match the queryset's criteria.
11. exists() checks whether the queryset has any results.
12. values() returns a queryset of dictionaries, where each dictionary represents a single object and contains the specified fields.
13. select_related() retrieves related objects using a join operation, to avoid making multiple queries.
14. prefetch_related() retrieves related objects using separate queries, to avoid loading unnecessary data.
15. get() retrieves a single object from the database that matches the specified criteria. If no object is found, raises a DoesNotExist exception.
16. first() retrieves the first object in the queryset, or None if the queryset is empty.
17. last() retrieves the last object in the queryset, or None if the queryset is empty.
18. aggregate() performs aggregate calculations on the queryset, such as sum, average, and count.
19. create() creates a new object in the database and returns it.
20. update_or_create() updates an existing object if it exists, or creates a new object if it does not.
21. values_list() returns a queryset of tuples, where each tuple represents a single object and contains the specified fields.
22. only() restricts the fields that are retrieved from the database, to optimize performance.
23. defer() defers the loading of certain fields until they are actually accessed, to optimize performance.
24. exclude() retrieves a subset of objects that do not match a certain criteria.
25. distinct() returns a queryset with distinct results.
26. iterator() retrieves objects from the database one at a time, to reduce memory usage.
27. in_bulk() retrieves a dictionary of objects, keyed by their primary keys.
28. select_for_update() locks the selected rows in the database, to prevent concurrent updates.


### How to ###

- delete every instance of a Django model, you can use the delete() method on the queryset of the model. Here is an example:

```python

from myapp.models import MyModel

MyModel.objects.all().delete()
```

In this example, MyModel is the name of the Django model that you want to delete all instances of. The objects attribute of the model provides a queryset manager that you can use to retrieve and manipulate instances of the model. The all() method of the queryset returns all instances of the model, and the delete() method deletes them from the database.

It's important to note that the delete() method does not call the delete() method on each individual instance of the model. Instead, it executes a single SQL query that deletes all instances at once. This can be more efficient than deleting instances one by one, especially if there are a large number of instances.

### Foreign Keys ###



### One to many relationship ###

To implement a one-to-many relationship in Django models, you can use the ForeignKey field. The ForeignKey field is used to create a relationship between two models.

Here's an example:

```python
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=50)

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
```

In this example, we have two models: Author and Book. The Book model has a ForeignKey field that references the Author model. This creates a one-to-many relationship between Author and Book.

The on_delete parameter specifies what should happen when an Author instance is deleted. In this case, we use models.CASCADE, which means that when an Author instance is deleted, all associated Book instances will also be deleted.

The related_name parameter allows you to specify the name of the reverse relation from Author to Book. In this case, we use books as the related name, so we can access all the books of an author like this:

```python
author = Author.objects.get(pk=1)
books = author.books.all()
```

This will return all the books associated with the author.
