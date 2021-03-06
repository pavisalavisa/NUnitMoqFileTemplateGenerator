using FluentAssertions;
using NUnit.Framework;
using System.Collections.Generic;
using Moq;

namespace InsertProjectNameHere.Tests
{
	[TestFixture]
	public class ExampleServiceTests
	{
		private Mock<IRepository<Employee>> _studentRepository;
		private Mock<IRepository<StudentCourse>> _studentCourseRepository;
		private Mock<IRepository<Course>> _courseRepository;

		private ExampleService _service;

		[SetUp]
		public void SetUp()
		{
			_studentRepository = new Mock<IRepository<Employee>>();
			_studentCourseRepository = new Mock<IRepository<StudentCourse>>();
			_courseRepository = new Mock<IRepository<Course>>();
		
			_service = new ExampleService(_studentRepository.Object,_studentCourseRepository.Object,_courseRepository.Object);
		}
	}
}