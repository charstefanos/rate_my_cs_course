import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','rate_my_cs_course.settings')

import django
django.setup()
from csapp.models import Course


def populate():
    YEAR_IN_UNI_CHOICES = (
    ('Undergraduate', (
            ('UNDERGRAD_1YEAR', 'Undergraduate (year 1)'),
            ('UNDERGRAD_2YEAR', 'Undergraduate (year 2)'),
            ('UNDERGRAD_3YEAR', 'Undergraduate (year 3)'),
            ('UNDERGRAD_4YEAR', 'Undergraduate (year 4)'),
        )
    ),
    ('Postgraduate', (
            ('POSTGRAD', 'Postgraduate'),
        )
    ),
    )
    undergraduate_1year_courses = [
        {'name': '1CT INTRODUCTION TO COMPUTATIONAL THINKING COMPSCI1016', 
        'description': 'Computational processes are increasingly being discovered in natural, social and economic systems as well as typical silicon-based computing devices such as laptops and smartphones. For those with little or no previous computing education, this course develops the necessary understanding and thinking skills so that such systems can be viewed as predictable, understandable and ultimately controllable. It is valuable in its own right, as an underpinning now required in many other disciplines, and as a foundation for further study in Computing Science.',
        'year_in_university': YEAR_IN_UNI_CHOICES[0][1][0]},
        {'name': '1S SYSTEMS COMPSCI1018', 
        'description': 'CS1S introduces the fundamentals of computer systems, including representation of information, digital circuits, processor organisation, machine language, and the relation between hardware and software systems.',
        'year_in_university': YEAR_IN_UNI_CHOICES[0][1][0]},
        {'name':'1F - COMPUTING FUNDAMENTALS COMPSCI1006',
        'description':'The aim of the CS1F course is to give students an understanding of human-computer interaction (styles of interaction, requirements for an interactive system in relation to the nature of the tasks being supported, issues in the design of interactive systems, critical assessment of designs); the ways in which databases contribute to the management of large amounts of data, the professional and ethical issues raised by the existence of databases and networks.',
        'year_in_university': YEAR_IN_UNI_CHOICES[0][1][0]},
        {'name':'COMPUTING SCIENCE 1P (STANDARD ROUTE) COMPSCI1001',
        'description':'The CS1P course is designed for students with good foundational computational thinking skills - that is, a solid understanding of basic programming concepts and the ability to solve simple unseen programming problems from scratch with no assistance. The course reviews this foundation and then builds on it by developing students ability to reason about elements of the software development process, including for example, complexity of algorithms, rigorous testing techniques and problem solving methodologies.',
        'year_in_university': YEAR_IN_UNI_CHOICES[0][1][0]},
        {'name':'COMPUTING SCIENCE 1P (HALF COURSE) COMPSCI1005',
        'description':'The aim of the CS1P (Half) course is to produce programmers equipped with an understanding of: Fundamental computational concepts underlying most programming languages; A range of problem-solving techniques using computers; The skills supporting the solution of small problems using a programming language; The clear expression of solutions at different levels of abstraction.',
        'year_in_university': YEAR_IN_UNI_CHOICES[0][1][0]},
        {'name':'COMPUTING SCIENCE 1PX (ALTERNATE ROUTE) COMPSCI1017',
        'description':'This course assumes core computational thinking skills and is designed to be a natural follow-on from the CS1CT course for those who decide they wish to continue their study of Computing Science. The course develops students ability to reason about elements of the software development process, including for example, complexity of algorithms, rigorous testing techniques and problem solving methodologies.',
        'year_in_university': YEAR_IN_UNI_CHOICES[0][1][0]},
        {'name':'FOUNDATIONS OF PROFESSIONAL SOFTWARE ENGINEERING COMPSCI1019',
        'description':'Students on the GA programme will be going straight into a working environment, so it is important that they understand the fundamentals of working as a professional. This course will introduce them to many facets of software development beyond simply writing code, which will be important to prepare them for professional work.',
        'year_in_university': YEAR_IN_UNI_CHOICES[0][1][0]}
    ]
    undergraduate_2year_courses = [    
        {'name':'ALGORITHMIC FOUNDATIONS 2 COMPSCI2003',
        'description':'To introduce the foundational mathematics needed for Computing Science; To make students proficient in their use; To show how they can be applied to advantage in understanding computational phenomena.',
        'year_in_university': YEAR_IN_UNI_CHOICES[0][1][1]},
        {'name':'ALGORITHMS & DATA STRUCTURES 2 COMPSCI2007',
        'description':'To familiarise students with fundamental data types and data structures used in programming, with the design and analysis of algorithms for the manipulation of such structures, and to provide practice in the implementation and use of these structures and algorithms in a Java context.',
        'year_in_university':YEAR_IN_UNI_CHOICES[0][1][1]}
    ]
    undergraduate_3year_courses = [
        {'name':'SOFTWARE ENGINEERING M3 COMPSCI3005',
        'description':'An introduction to software engineering principles, processes and techniques.',
        'year_in_university':YEAR_IN_UNI_CHOICES[0][1][2]},
        {'name':'TEAM PROJECT 3 COMPSCI3004',
        'description':'This course gives students the experience of working on a substantial team based software project. The course provides the opportunity to apply the principles, practices and tools learned during the associated Professional Software Development (H) course.',
        'year_in_university':YEAR_IN_UNI_CHOICES[0][1][2]}
    ]
    undergraduate_4year_courses = [
        {'name':'ADVANCED NETWORKED SYSTEMS (H) COMPSCI4083',
        'description':'The course aims to give students a deep understanding of the fundamental design, implementation, management, and evaluation principles that govern large-scale, high-speed networked systems. These include algorithmic and implementation techniques for high-speed networking in routers and end-nodes; systems performance measurement and modelling principles; network and system resource management, allocation and engineering schemes; and research and technological advances that drive the development of a converged, global telecommunications medium of the future.',
        'year_in_university':YEAR_IN_UNI_CHOICES[0][1][3]},
        {'name':'ADVANCED NETWORKING AND COMMUNICATIONS (H) COMPSCI4002',
        'description':'This course adds depth and some breadth to the material covered in Networked Systems (H). Advanced Networking and Communications (H) will show how fundamental principles of communications theory underpin the structures of the global telecommunications network and the Internet and determine the logic of how these networks interact.',
        'year_in_university':YEAR_IN_UNI_CHOICES[0][1][3]}
    ]
    postgraduate_courses = [
        {'name':'ADVANCED PROGRAMMING (M) COMPSCI5002',
        'description':'The course is intended to extend the students knowledge to encompass a number of important programming techniques necessary for building a modern computing application. The course content will include techniques in Java to deal with a range of issues drawn from the following: program design using an object oriented programming model; modelling data using programming language type systems; event and exception programming; providing a graphical user interface; thread programming; persistence; and distributed programming. It will also cover in brief the underlying Java run time system and techniques found in other languages.',
        'year_in_university':YEAR_IN_UNI_CHOICES[1][1][0]}
    ]
    
    all_courses = [undergraduate_1year_courses,undergraduate_2year_courses,undergraduate_3year_courses,undergraduate_4year_courses,postgraduate_courses]


    # The code below goes through the all_courses list, then for each sublist, adds the courses.
    for cat in all_courses:
        for course in cat:
            add_course(course['name'], course['description'], course['year_in_university'])
            
    # Print out the courses we have added.
    for c in Course.objects.all():
            print(f'{c}')


def add_course(name, description, year_in_university):
    c = Course.objects.get_or_create(name=name)[0]
    c.description=description
    c.year_in_university=year_in_university
    c.save()
    return c

# Start execution here!
if __name__ == '__main__':
    print('Starting CSapp population script...')
    populate()