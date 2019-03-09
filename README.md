# NUnitMoqFileTemplateGenerator
Generate unit test template based on given service

Provides boilerplate code needed for unit tests based of NUnit testing framework along with Moq mocking framework. 
Exercising dependency injection comes with a price of having to manually set up and mock many dependencies which 
becomes tedious as soon as number of dependencies hits 2 (which is very often).

Usage: python main.py <path_to_your_cs_file>
Example: python main.py ExampleService.cs
