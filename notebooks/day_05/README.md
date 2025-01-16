Day 5 Challenge: Introduction to Object-Oriented Programming (OOP)

Topics:

1. Introduction to OOP
   - What is OOP?
   - Benefits of OOP
   - OOP vs Procedural Programming

2. Classes and Objects
   - Defining a class
   - Creating objects (instances)
   - Class attributes vs instance attributes
   - The `self` parameter

3. Methods
   - Instance methods
   - Class methods (using `@classmethod` decorator)
   - Static methods (using `@staticmethod` decorator)

4. Constructors and Destructors
   - `__init__` method
   - `__del__` method

5. Encapsulation
   - Public, private, and protected attributes
   - Getter and setter methods
   - Property decorators

6. Inheritance
   - Single inheritance
   - Multiple inheritance
   - Method overriding
   - The `super()` function

7. Polymorphism
   - Method overloading (function overloading in Python)
   - Method overriding
   - Duck typing

8. Abstract Base Classes and Interfaces
   - `abc` module
   - Abstract methods
   - Concrete methods in abstract classes

9. Advanced OOP Concepts
   - Composition vs Inheritance
   - Method Resolution Order (MRO)
   - Mixins

Exercises:

1. Basic Class Creation:
   Create a `Person` class with attributes for name, age, and address. Include methods to update these attributes and a method to print a person's details.

2. Bank Account System:
   Implement a `BankAccount` class with methods for deposit, withdrawal, and checking balance. Include proper error handling for insufficient funds.

3. Shape Hierarchy:
   Create a base `Shape` class and derive classes like `Circle`, `Rectangle`, and `Triangle`. Implement methods to calculate area and perimeter for each shape.

4. Employee Management System:
   Design a system with classes for `Employee`, `Manager`, and `Executive`. Use inheritance to represent the hierarchy. Include methods for calculating salaries, assigning tasks, and generating reports.

5. Library Management System:
   Create classes for `Book`, `Library`, and `Member`. Implement methods for checking out books, returning books, and managing library inventory. Use composition to represent the relationship between `Library` and `Book`.

6. Polymorphism Exercise:
   Create a `Vehicle` base class and derive classes like `Car`, `Motorcycle`, and `Truck`. Implement a `start_engine()` method in each class that behaves differently.

7. Abstract Class Implementation:
   Design an abstract `Animal` class with abstract methods like `speak()` and `move()`. Create concrete classes like `Dog`, `Cat`, and `Bird` that implement these methods.

8. Advanced OOP Project: E-Commerce System
   Develop a comprehensive e-commerce system that demonstrates mastery of OOP concepts. Include the following components:

   - `Product` class with attributes like name, price, and inventory
   - `User` class with subclasses for `Customer` and `Admin`
   - `ShoppingCart` class that can hold multiple products
   - `Order` class to process and track customer orders
   - `PaymentProcessor` abstract class with concrete implementations for different payment methods
   - `InventoryManager` class to handle stock updates
   - Implement appropriate relationships (inheritance, composition) between classes
   - Use encapsulation to protect sensitive data (e.g., payment information)
   - Implement polymorphic behavior where appropriate (e.g., payment processing)
   - Include proper error handling and input validation

Notes:
- Focus on writing clean, readable, and well-documented code
- Use meaningful variable and method names
- Practice proper indentation and code organization
- Implement error handling where appropriate
- Think about real-world analogies to understand OOP concepts better
- Don't hesitate to refactor your code as you learn new concepts

Additional Resources:
- Python Official Documentation on Classes: https://docs.python.org/3/tutorial/classes.html
- Real Python's OOP in Python 3: https://realpython.com/python3-object-oriented-programming/
- "Python Object-Oriented Programming" by Dusty Phillips (book)

Remember to test your code thoroughly and experiment with different scenarios. OOP is a powerful paradigm, and mastering it will significantly enhance your Python programming skills. Good luck with your Day 5 challenge!
