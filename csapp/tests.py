import os
import socket
import populate_csapp
import json
from django.urls import reverse, resolve
from django.test import TestCase
from django.contrib.staticfiles import finders
from csapp.forms import *
from django.contrib.auth.models import User
from django.conf import settings
from csapp.models import *
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client

class UserProfileModelTest(TestCase):

    def test_can_create_user(self):
        user = User.objects.create(username='test_student')
        user.set_password('123456')
        user.save()

        users_in_database = User.objects.all()
        self.assertEqual(users_in_database[0], user, msg = "Could not create user")
        
    def test_can_create_profile(self):

        course = Course(name='test course year 1', description='test description',
                        year_in_university=1, views = 1)
        course.save()
        
        user = User.objects.create(username='test_student')
        user.set_password('123456')
        user.save()

        profile = UserProfile.objects.create(user=user)
        profile.first_name = 'Test'
        profile.last_name = 'Student'
        profile.email = 'test.student@csapp.com'
        profile.year_of_studies = 1
        profile.courses.add = course
        profile.contact = True
        profile.save()

        profiles_in_database = UserProfile.objects.all()
        self.assertEqual( profiles_in_database[0], profile, msg = "Could not create profile")

    def test_profile_can_login(self):
        course = Course(name='test course year 1', description='test description',
                        year_in_university=1, views = 1)
        course.save()
        
        user = User.objects.create(username='test_student')
        user.set_password('123456')
        user.save()

        profile = UserProfile.objects.create(user=user)
        profile.first_name = 'Test'
        profile.last_name = 'Student'
        profile.email = 'test.student@csapp.com'
        profile.year_of_studies = 1
        profile.courses.add = course
        profile.contact = True
        profile.save()

        client = Client()
        logged_in = client.login(username='test_student', password='123456')
        self.assertTrue(logged_in, msg = "Could not log in")
     
class CourseModelTest(TestCase):
    
    def test_can_create_course(self):
        #create test course
        course = Course(name='test course year 1', description='test description',
                        year_in_university=1, views = 1)
        course.save()
        course_in_database = Course.objects.all()
        course_in_database = course_in_database[0]
        self.assertEqual(course_in_database, course, msg = "Could not create course")

    def test_course_contains_slug_field(self):
        #create test course
        course = Course(name='test course year 1', description='test description',
                        year_in_university=1, views = 1)
        course.save()
        #check if slug was saved
        self.assertEqual(course.slug, 'test-course-year-1', msg = "Course slug is incorrect")

    def test_str_representation(self):
        #create test course
        course = Course(name='test course year 1', description='test description',
                        year_in_university=1, views = 1)
        course.save()
        #check if the method __str__ returns the course name
        self.assertEqual(str(course), course.name, msg = "Course string representation is wrong")

class CourseRatingModelTest(TestCase):

    def setUp(self):
        #create test course
        self.course = Course(name='test course year 1', description='test description',
                        year_in_university=1, views = 1)
        self.course.save()
        #create test student and login
        self.student = User.objects.create(username='test_student', password='123456')
        self.student_profile = UserProfile.objects.create(user=self.student)
        self.student_profile.first_name = 'Test'
        self.student_profile.last_name = 'Student'
        self.student_profile.email = 'test.student@csapp.com'
        self.student_profile.year_of_studies = 1
        self.student_profile.courses.add = self.course
        self.student_profile.contact = True
        self.client.login(username='test_student', password='123456')
        
    def test_can_create_review(self):
        #create test review
        review = CourseRating(student=self.student_profile, course=self.course)
        review.overall_rating = 1
        review.lecturer_rating = 1
        review.engagement = 1
        review.informative = 1
        review.comment = 'test comment'
        review.save()
        #check if review exists in database
        reviews_in_database = CourseRating.objects.all()
        reviews_in_database = reviews_in_database[0]
        self.assertEqual(reviews_in_database, review, msg = "Could not create review")

    def test_verbose_name_plural(self):
        self.assertEqual(str(CourseRating._meta.verbose_name_plural), "Course Ratings", msg = "Wrong plural")

class TestViews(TestCase):

    def create_course(self, name='test course year 1', description='test description',
                        year_in_university=1, views = 1):
        return Course.objects.create(name=name, description=description,
             year_in_university=year_in_university, views=views, slug='test-course-year-1')
    def setUp(self):
        #create test course
        self.course = Course(name='test course year 1', description='test description',
                        year_in_university=1, views = 1)
        self.course.save()
        #create test student and login
        self.student = User.objects.create(username='test_student', password='123456')
        self.student_profile = UserProfile.objects.create(user=self.student)
        self.student_profile.first_name = 'Test'
        self.student_profile.last_name = 'Student'
        self.student_profile.email = 'test.student@csapp.com'
        self.student_profile.year_of_studies = 1
        self.student_profile.courses.add = self.course
        self.student_profile.contact = True
        self.client.login(username='test_student', password='123456')

    def test_home_view(self):
        url = reverse("home")
        resp = self.client.get(url)
        #Check the response code is 200
        self.assertEqual(resp.status_code, 200, msg = "Wrong status code")

    def test_undergraduate_view(self):
        url = reverse("csapp:undergraduate")
        resp = self.client.get(url)
        #Check the response code is 200
        self.assertEqual(resp.status_code, 200, msg = "Wrong status code")

    def test_postgraduate_view(self):
        url = reverse("csapp:postgraduate")
        resp = self.client.get(url)
        #Check the response code is 200
        self.assertEqual(resp.status_code, 200, msg = "Wrong status code")

    def test_course_view(self):
        url = reverse("csapp:course", kwargs={'course_name_slug': 'test-course-year-1'})
        resp = self.client.get(url)
        #Check the response code is 200
        self.assertEqual(resp.status_code, 200, msg = "Wrong status code")
    
    def test_about_view(self):
        url = reverse("csapp:about")
        resp = self.client.get(url)
        #Check the response code is 200
        self.assertEqual(resp.status_code, 200, msg = "Wrong status code")

    def test_register_view(self):
        url = reverse("csapp:register")
        resp = self.client.get(url)
        #Check the response code is 200
        self.assertEqual(resp.status_code, 200, msg = "Wrong status code")

    def test_user_login_view(self):
        url = reverse("csapp:login")
        resp = self.client.get(url)
        #Check the response code is 200
        self.assertEqual(resp.status_code, 200, msg = "Wrong status code")

    def test_opendays_view(self):
        url = reverse("csapp:opendays")
        resp = self.client.get(url)
        #Check the response code is 302
        self.assertEqual(resp.status_code, 302, msg = "Wrong status code")

    def test_profile_view(self):
        url = reverse("csapp:profile")
        resp = self.client.get(url)
        #Check the response code is 302
        self.assertEqual(resp.status_code, 302, msg = "Wrong status code")

    def test_write_review_view(self):
        url = reverse("csapp:write_review", kwargs={'course_name_slug': 'test-course-year-1'})
        resp = self.client.get(url)
        #Check the response code is 302
        self.assertEqual(resp.status_code, 302, msg = "Wrong status code")

    def test_my_reviews_view(self):
        url = reverse("csapp:my_reviews")
        resp = self.client.get(url)
        #Check the response code is 302
        self.assertEqual(resp.status_code, 302, msg = "Wrong status code")

class PopulationScriptTest(TestCase):
    def test_population_script_changes_databases(self):
        #Populate database
        populate_csapp.populate()

        #Check courses for year 1 are correct
        course = Course.objects.get(name='1CT INTRODUCTION TO COMPUTATIONAL THINKING COMPSCI1016')
        self.assertEqual(course.description, 'Computational processes are increasingly being discovered in natural, social and economic systems as well as typical silicon-based computing devices such as laptops and smartphones. For those with little or no previous computing education, this course develops the necessary understanding and thinking skills so that such systems can be viewed as predictable, understandable and ultimately controllable. It is valuable in its own right, as an underpinning now required in many other disciplines, and as a foundation for further study in Computing Science.')
        self.assertEqual(course.year_in_university, 1)

        course = Course.objects.get(name='1S SYSTEMS COMPSCI1018')
        self.assertEqual(course.description,'CS1S introduces the fundamentals of computer systems, including representation of information, digital circuits, processor organisation, machine language, and the relation between hardware and software systems.',)
        self.assertEqual(course.year_in_university, 1)

        course = Course.objects.get(name='1F - COMPUTING FUNDAMENTALS COMPSCI1006')
        self.assertEqual(course.description,'The aim of the CS1F course is to give students an understanding of human-computer interaction (styles of interaction, requirements for an interactive system in relation to the nature of the tasks being supported, issues in the design of interactive systems, critical assessment of designs); the ways in which databases contribute to the management of large amounts of data, the professional and ethical issues raised by the existence of databases and networks.',)
        self.assertEqual(course.year_in_university, 1)

        course = Course.objects.get(name='COMPUTING SCIENCE 1P (STANDARD ROUTE) COMPSCI1001')
        self.assertEqual(course.description,'The CS1P course is designed for students with good foundational computational thinking skills - that is, a solid understanding of basic programming concepts and the ability to solve simple unseen programming problems from scratch with no assistance. The course reviews this foundation and then builds on it by developing students ability to reason about elements of the software development process, including for example, complexity of algorithms, rigorous testing techniques and problem solving methodologies.',)
        self.assertEqual(course.year_in_university, 1)

        course = Course.objects.get(name='COMPUTING SCIENCE 1P (HALF COURSE) COMPSCI1005')
        self.assertEqual(course.description, 'The aim of the CS1P (Half) course is to produce programmers equipped with an understanding of: Fundamental computational concepts underlying most programming languages; A range of problem-solving techniques using computers; The skills supporting the solution of small problems using a programming language; The clear expression of solutions at different levels of abstraction.')
        self.assertEqual(course.year_in_university, 1)

        course = Course.objects.get(name='PRACTICAL ALGORITHMS COMPSCI1021')
        self.assertEqual(course.description, 'This course is designed to impart a breadth of knowledge on data structures, particularly with respect to the mathematical foundations involved in manipulating them. In doing so, it will also introduce students to foundational mathematical concepts in computing that will help them to better understand efficient programming and will provide a basis on which to build more complex mathematical concepts in later years of study.')
        self.assertEqual(course.year_in_university, 1)

        #Check courses for year 2 are correct
        course = Course.objects.get(name='OBJECT-ORIENTED SOFTWARE ENGINEERING 2 COMPSCI2008')
        self.assertEquals(course.description, 'This course introduces the basic concepts of software engineering. Students will learn methods for the design, implementation, testing and documentation of larger object-oriented programs, and will also develop program comprehension and design skills by studying and extending existing programs.')
        self.assertEquals(course.year_in_university, 2)

        course = Course.objects.get(name='ALGORITHMIC FOUNDATIONS 2 COMPSCI2003')
        self.assertEquals(course.description, 'To introduce the foundational mathematics needed for Computing Science; To make students proficient in their use; To show how they can be applied to advantage in understanding computational phenomena.')
        self.assertEquals(course.year_in_university, 2)

        course = Course.objects.get(name='ALGORITHMS & DATA STRUCTURES 2 COMPSCI2007')
        self.assertEquals(course.description, 'To familiarise students with fundamental data types and data structures used in programming, with the design and analysis of algorithms for the manipulation of such structures, and to provide practice in the implementation and use of these structures and algorithms in a Java context.')
        self.assertEquals(course.year_in_university, 2)

        course = Course.objects.get(name='JAVA PROGRAMMING 2 COMPSCI2001')
        self.assertEquals(course.description, 'This course extends students experience in programming using a strongly typed language (Java) and strengthens their problem solving skills. Students will learn the ideas that underpin object-oriented programming and will apply those concepts in developing small and medium sized software systems. Students will also learn to select and re-use existing software components and libraries, and will gain experience in concurrent programming and elementary graphical user-interface (GUI) development.')
        self.assertEquals(course.year_in_university, 2)

        course = Course.objects.get(name='NETWORKS AND OPERATING SYSTEMS ESSENTIALS 2 COMPSCI2024')
        self.assertEquals(course.description, 'The course will introduce students to essential topics in computer networks and operating systems. It has a focus on the underlying concepts, design, and operation of the Internet, and on the role, basic features, and principles of computer operating systems.')
        self.assertEquals(course.year_in_university, 2)

        course = Course.objects.get(name='WEB APPLICATION DEVELOPMENT 2 COMPSCI2021')
        self.assertEquals(course.description, 'The aim of this course is to provide students with a comprehensive overview of web application development. It will provide students with the skills to design and develop distributed web applications in a disciplined manner, using a range of tools and technologies. It will also strengthen their understanding of the context and rationale of distributed systems. ')
        self.assertEquals(course.year_in_university, 2)

        #Check courses for year 3 are correct
        course = Course.objects.get(name='SOFTWARE ENGINEERING M3 COMPSCI3005')
        self.assertEquals(course.description, 'An introduction to software engineering principles, processes and techniques.')
        self.assertEquals(course.year_in_university, 3)

        course = Course.objects.get(name='TEAM PROJECT 3 COMPSCI3004')
        self.assertEquals(course.description, 'This course gives students the experience of working on a substantial team based software project. The course provides the opportunity to apply the principles, practices and tools learned during the associated Professional Software Development (H) course.')
        self.assertEquals(course.year_in_university, 3)

        #Check courses for year 4 are correct
        course = Course.objects.get(name='ADVANCED SOFTWARE ENGINEERING PRACTICES (H) COMPSCI4071')
        self.assertEquals(course.description, 'This course gives students the opportunity to learn and practice advanced principles, methods and tools in Software Engineering.  The course is intended for students who have experience of software development through a summer internship or similar. The course covers technical and management skills that are needed for mentoring and leading teams of software developers. The course is delivered in collaboration with an established software industry partner (JP Morgan).')
        self.assertEquals(course.year_in_university, 4)

        course = Course.objects.get(name='ADVANCED NETWORKED SYSTEMS (H) COMPSCI4083')
        self.assertEquals(course.description, 'The course aims to give students a deep understanding of the fundamental design, implementation, management, and evaluation principles that govern large-scale, high-speed networked systems. These include algorithmic and implementation techniques for high-speed networking in routers and end-nodes; systems performance measurement and modelling principles; network and system resource management, allocation and engineering schemes; and research and technological advances that drive the development of a converged, global telecommunications medium of the future.')
        self.assertEquals(course.year_in_university, 4)

        course = Course.objects.get(name='ADVANCED NETWORKING AND COMMUNICATIONS (H) COMPSCI4002')
        self.assertEquals(course.description, 'This course adds depth and some breadth to the material covered in Networked Systems (H). Advanced Networking and Communications (H) will show how fundamental principles of communications theory underpin the structures of the global telecommunications network and the Internet and determine the logic of how these networks interact.')
        self.assertEquals(course.year_in_university, 4)

        course = Course.objects.get(name='COMPUTER VISION METHODS AND APPLICATIONS (H) COMPSCI4066')
        self.assertEquals(course.description, 'The Computer Vision Methods and Applications (CVMA) course is intended to equip students with the necessary theoretical and practical understanding of image processing and computer vision techniques to enable them to meet the challenges of building advanced image-based applications. Examples of potential vision-based applications include: image understanding in mobile devices (cameras, phones, tablet computers etc.), robot vision systems, autonomous vehicle guidance and road monitoring, driver attention monitoring, image database query systems, creative media production tools, interactive gaming, augmented reality and visual biometrics, forensic image analysis, security and surveillance, and medical imaging. The course will focus on the application of recent advances in Computer Vision techniques that underpin a wide variety of systems and products based on methods such as: face detection, object recognition, tracking, segmentation and 3D imaging.')
        self.assertEquals(course.year_in_university, 4)

        course = Course.objects.get(name='DATA FUNDAMENTALS (H) COMPSCI4073')
        self.assertEquals(course.description, 'This course will cover computational approaches to working with numerical data on a large scale. Computation on arrays of continuous variables underpins machine learning, information retrieval, data analytics, computer vision and signal processing. This course will cover vectorised operations on numerical arrays, fundamental stochastic and probabilistic methods and scientific visualisation.')
        self.assertEquals(course.year_in_university, 4)

        course = Course.objects.get(name='MOBILE HUMAN-COMPUTER INTERACTION (SIT) SIT4047')
        self.assertEquals(course.description, 'Mobile Human-Computer Interaction (SIT) gives students an overview of the fields of mobile HCI and ubiquitous computing, and an understanding of the practical challenges associated with embedded software development for mobile interactive systems, and associated services.')
        self.assertEquals(course.year_in_university, 4)

        #Check courses for postgraduates are correct
        course = Course.objects.get(name='ADVANCED PROGRAMMING (M) COMPSCI5002')
        self.assertEquals(course.description, 'The course is intended to extend the students knowledge to encompass a number of important programming techniques necessary for building a modern computing application. The course content will include techniques in Java to deal with a range of issues drawn from the following: program design using an object oriented programming model; modelling data using programming language type systems; event and exception programming; providing a graphical user interface; thread programming; persistence; and distributed programming. It will also cover in brief the underlying Java run time system and techniques found in other languages.')
        self.assertEquals(course.year_in_university, 5)

        course = Course.objects.get(name='BIG DATA: SYSTEMS, PROGRAMMING, AND MANAGEMENT (M) COMPSCI5088')
        self.assertEquals(course.description, 'Big Data is nowadays manifested in a very large number of environments and application fields pertaining to our education, entertainment, health, public governance, enterprising, etc. The course will endow students with the understanding of the new challenges big data introduces and the currently available solutions. These include (i) challenges pertaining to the modelling, accessing, and storing of big data, (ii) an understanding of the fundamentals of systems designed to store and access big data, and (iii) programming paradigms for efficient scalable access to big data.')
        self.assertEquals(course.year_in_university, 5)

        course = Course.objects.get(name='CRYPTOGRAPHY AND SECURE DEVELOPMENT (M) COMPSCI5079')
        self.assertEquals(course.description, 'A course on cryptographic algorithms and how to develop code for secure systems.')
        self.assertEquals(course.year_in_university, 5)

        course = Course.objects.get(name='DEEP LEARNING (M) COMPSCI5085')
        self.assertEquals(course.description, 'This course is the next step beyond our introductory machine learning course and teaches students about modern techniques for machine learning with high-dimensional image and sequence (time-series) data, and the underlying computational structures for such systems.')
        self.assertEquals(course.year_in_university, 5)

        course = Course.objects.get(name='HUMAN-CENTRED SECURITY (M) COMPSCI5060')
        self.assertEquals(course.description, 'This course teaches you the design and evaluation of usable, secure and privacy aware systems.')
        self.assertEquals(course.year_in_university, 5)

        course = Course.objects.get(name='MOBILE HUMAN-COMPUTER INTERACTION (M) COMPSCI5015')
        self.assertEquals(course.description, 'Mobile Human-Computer Interaction (M) gives students an overview of the fields of mobile HCI and ubiquitous computing, and an understanding of the practical challenges associated with embedded software development for mobile interactive systems, and associated services.')
        self.assertEquals(course.year_in_university, 5)

        #Check year 1 students have corrent information
        student_user = User.objects.get(username='Arthur')
        student = UserProfile.objects.get(user=student_user)
        self.assertEquals(student.first_name, 'Arthur', msg = "Wrong first name")
        self.assertEquals(student.last_name, 'Tull', msg = "Wrong last name")
        self.assertEquals(student.email, 'ArthurMTull@rhyta.com', msg = "Wrong email")
        self.assertEquals(student.current_student, True, msg = "Wrong choice for current student")
        self.assertEquals(student.year_of_studies, 1, msg = "Wrong year of studies")

        coursesThatShouldBeTaken = Course.objects.filter(name__in = ['1CT INTRODUCTION TO COMPUTATIONAL THINKING COMPSCI1016',
                                                                     '1S SYSTEMS COMPSCI1018',
                                                                     '1F - COMPUTING FUNDAMENTALS COMPSCI1006',
                                                                     'COMPUTING SCIENCE 1PX (ALTERNATE ROUTE) COMPSCI1017',
                                                                     'SPATIAL SKILLS TRAINING 1 COMPSCI1026'])
        self.assertQuerysetEqual(student.courses.all(), map(repr, coursesThatShouldBeTaken), ordered=False, msg = "Courses do not match")
        self.assertEqual(student.contact, True, msg = "Wrong contact choice")

class UserFormTest(TestCase):
    def test_user_form_valid_data(self):
        #create form
        form = UserForm({'username': 'test', 'password': '123456'})
        self.assertTrue(form.is_valid(), msg = "Form is not valid")

class UserProfileFormTest(TestCase):
    def test_user_profile_form_valid_data(self):
        #create form
        form = UserProfileForm({'first_name': 'Name', 'last_name': 'Last', 'email': 'test@hotmail.com', 'current_student':False})
        self.assertTrue(form.is_valid(), msg = "Form is not valid")

    def test_user_profile_form_invalid_data(self):
        #create form
        form = UserProfileForm({'first_name': 'Name', 'last_name': 'Last', 'email': 'test', 'current_student':False})
        self.assertFalse(form.is_valid(), msg = "Form is valid")

class ReviewFormTest(TestCase):
    def setUp(self):
        #create test course
        self.course = Course(name='test course year 1', description='test description',
                        year_in_university=1, views = 1)
        self.course.save()
        #create test student and login
        self.student = User.objects.create(username='test_student', password='123456')
        self.student_profile = UserProfile.objects.create(user=self.student)
        self.student_profile.first_name = 'Test'
        self.student_profile.last_name = 'Student'
        self.student_profile.email = 'test.student@csapp.com'
        self.student_profile.year_of_studies = 1
        self.student_profile.courses.add = self.course
        self.student_profile.contact = True

    def test_review_form_valid_data(self):
        #login as test student
        self.client.login(username='test_student', password='123456')
        #create form
        form = ReviewForm({'overall_rating': 1, 'lecturer_rating': 2, 'engagement': 3,
            'informative': 4, 'comment': 'test comment'})
        self.assertTrue(form.is_valid(), msg = "Form is not valid")

    def test_review_form_invalid_data(self):
        #login as test student
        self.client.login(username='test_student', password='123456')
        #create form
        form = ReviewForm({'overall_rating': 1, 'lecturer_rating': 2, 'engagement': 0,
            'informative': 4, 'comment': 'test comment'})
        self.assertFalse(form.is_valid(), msg = "Form is valid")

    def test_review_form_adds_data(self):
        #login as test student
        self.client.login(username='test_student', password='123456')
        #create form
        form = ReviewForm({'overall_rating': 1, 'lecturer_rating': 2, 'engagement': 3,
            'informative': 4, 'comment': 'test comment'})
        #save form
        review = form.save(commit=False)
        course = Course.objects.all().get(name = self.course.name)
        review.course = course
        review.student = UserProfile.objects.all().get(user=User.objects.get(username='test_student'))
        review.save()
        #get user profile
        user =UserProfile.objects.all().get(user=User.objects.get(username='test_student'))
        #get all reviews check the reviews with the above data that exists
        review = CourseRating.objects.all().get(course=course, student=user)
        self.assertIsNotNone(review, msg = "Form does not save data")


        
