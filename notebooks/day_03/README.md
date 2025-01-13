# Day 3 Challenge: Functions and Modules

## Topics:
1. Functions
   - Defining functions
   - Function parameters and arguments
   - Return statements
   - Default parameters
   - Keyword arguments
   - Variable-length arguments (*args and **kwargs)
   - Lambda functions
   - Scope and namespaces

2. Modules
   - What are modules?
   - Importing modules
   - Creating custom modules
   - The `if __name__ == "__main__":` idiom
   - Python standard library modules
   - Third-party modules and pip

## Exercises:
1. Create a function that calculates the area of a circle given its radius
2. Write a function that takes a variable number of arguments and returns their sum
3. Create a lambda function to sort a list of tuples based on the second element
4. Write a function with default parameters to generate a personalized greeting
5. Create a custom module with functions for basic arithmetic operations
6. Use the `random` module to create a simple number guessing game
7. Implement a function decorator that measures the execution time of a function

## Advanced Assignment: Weather Data Analyzer

Create a weather data analysis tool using modules. This project will involve creating multiple modules and using both built-in and third-party libraries.

Requirements:

1. Create a module `data_fetcher.py`:
   - Use the `requests` library to fetch weather data from a public API (e.g., OpenWeatherMap).
   - Include functions to fetch current weather and historical data.

2. Create a module `data_processor.py`:
   - Include functions to process and clean the fetched data.
   - Use `pandas` for data manipulation.

3. Create a module `data_analyzer.py`:
   - Include functions to perform statistical analysis on the weather data.
   - Calculate averages, identify trends, etc.

4. Create a module `data_visualizer.py`:
   - Use `matplotlib` to create visualizations of the weather data.
   - Include functions for different types of plots (line graphs, bar charts, etc.).

5. Create a main script `weather_analyzer.py`:
   - Import and use functions from all the above modules.
   - Implement a command-line interface for user interaction.
   - Allow users to specify a location, time range, and type of analysis/visualization.

6. Implement proper error handling and input validation throughout the project.

7. Use the `if __name__ == "__main__":` idiom in each module for any test code.

8. Include docstrings for all modules, classes, and functions.

## Notes:
- Pay attention to function naming conventions and docstrings
- Understand the difference between local and global scope
- Practice writing clean, modular code
- Explore the Python standard library to find useful modules for common tasks
- Remember to use meaningful names for functions and variables

## Additional Resources:
- [Python Official Documentation on Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)
- [Python Official Documentation on Modules](https://docs.python.org/3/tutorial/modules.html)
- [Real Python's Guide to Python Functions](https://realpython.com/defining-your-own-python-function/)
- [Python Module of the Week](https://pymotw.com/3/)

Remember, the goal is to understand how to create reusable code components and organize your code effectively. Functions and modules are fundamental to writing clean, maintainable Python programs. Happy coding!
