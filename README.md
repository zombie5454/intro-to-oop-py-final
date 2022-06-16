# Intro
This is the final project of OOP Group2. We implement a customized question database

It support:

* add/edit/delete question/question category
* export/import questions
* take exam

# Usage 
To use this database, please download all files, and make sure they are in the same directory, and run ``Main.py``

* the default database storage directory is "./a"
* to change this directory, modify ``Main.py``, line 14, ``self.model = Model("./a")`` to ``self.model = Model("path_you_want")``

To import questions, you can first try export one question bank and see the demand format of question bank

Above supported functions can be executed by clicking the corresponding buttons on the UI.

# File structure
UI/ : QtUI

View/: files for User Interface

Controller/: files for communication between user interface and logical data base (aka model)

Model/: files for physical database implementation, and communication between real data and controller

tests/: our test functions to debug

