# Restaurant Kitchen Service Project

Django project for managing cooks, dishes and dish types in a restaurant

## Check it out! 
[Restaurant project deployed to Render](https://restaurant-mate-n0wt.onrender.com/)

## Installation

Python3 must be already installed

```shell
git clone https://github.com/volodymyr-komarnyckyi/restaurant-kitchen-service
cd restaurant-kitchen-service
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS/Linux)
pip install -r requirements.txt
python manage.py runserver #starts Django Server
```

## Features

* Authentication functionality for Cook/User
* Managing cooks, dishes & dish types directly from website interface
* Powerful admin panel for advanced managing

## Default user for website

```
username: Volodymyr_cook
password: Volodymyr8204
```

## DB Structure

![Database Structure](db.png)

## Demo

![Website Interface](login.png)
![Website Interface](demo.png)
![Website Interface](cook_list.png)
![Website Interface](cook_detail(1).png)
![Website Interface](cook_detail(2).png)
![Website Interface](dish_list.png)
![Website Interface](dish_detail(cook).png)
![Website Interface](dish_detail(do_not_cook).png)
![Website Interface](dish_type_list.png)
![Website Interface](logout.png)
