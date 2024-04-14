from faker import Faker
import random

fake = Faker()

# Courses Available
courses = [
    "Introduction to Psychology", "World History: Ancient Civilizations", "Introduction to Sociology", "Introduction to Anthropology", "Philosophy: The Big Questions",
    "Literature and Society", "Art History: Renaissance to Modernism", "Music Appreciation: From Bach to Rock", "Introduction to Political Science",
    "Economics: Principles and Applications", "Environmental Science: An Introduction", "Introduction to Astronomy", "Chemistry: The Central Science", "Biology: Concepts and Investigations",
    "Physics: Principles and Applications", "Introduction to Computer Science", "Algorithms and Data Structures", "Introduction to Web Development", "Human-Computer Interaction",
    "Introduction to Artificial Intelligence", "Machine Learning Fundamentals", "Introduction to Digital Marketing", "Social Media Strategy and Analytics",
    "Introduction to Business Management", "Principles of Marketing", "Introduction to Financial Accounting", "Introduction to Microeconomics",
    "Introduction to Macroeconomics", "Introduction to International Relations", "Globalization and Culture", "Introduction to Cultural Anthropology",
    "Urban Sociology: Cities and Society", "Gender Studies: Perspectives and Debates", "Introduction to Linguistics", "Introduction to Philosophy of Science", "Ethics in Science and Technology",
    "Introduction to Environmental Ethics", "Biotechnology: Science and Society", "Cybersecurity Fundamentals", "Data Science for Social Sciences",
    "Geography: The Earth and Its People", "Health Psychology", "Introduction to Public Health", "Political Economy of Development", "Digital Humanities: Theory and Practice",
    "Introduction to Documentary Film", "Introduction to Creative Writing", "Digital Art and Design", "Introduction to Game Design", "Media Studies: Understanding Mass Media",
    "Introduction to Journalism", "Introduction to Human Rights", "Criminal Justice: Concepts and Issues", "Sociology of Religion", "Introduction to Archaeology",
    "Global Environmental Politics", "Philosophy of Mind", "Neuroscience: The Brain and Behavior", "Ecology and Conservation Biology", "Chemistry in Everyday Life",
    "Introduction to Renewable Energy", "Physics of Energy", "Introduction to Robotics", "Introduction to Space Exploration", "Introduction to Genetic Engineering",
    "Climate Change: Science and Solutions", "Introduction to Sustainable Development", "Introduction to Oceanography", "Astrophysics: Exploring the Universe",
    "Introduction to Quantum Mechanics", "Introduction to Nanotechnology", "Introduction to Biomedical Engineering", "Introduction to Cognitive Science",
    "Introduction to Cyber-Physical Systems", "Introduction to Data Visualization", "Introduction to Geographic Information Systems (GIS)", "Introduction to Remote Sensing",
    "Introduction to Statistical Analysis", "Introduction to Machine Learning with Python", "Introduction to Natural Language Processing", "Introduction to Computer Vision",
    "Introduction to Blockchain Technology", "Introduction to Cryptography", "Introduction to Network Security", "Introduction to Web Application Security",
    "Introduction to Cloud Computing", "Introduction to Internet of Things (IoT)", "Introduction to Virtual Reality (VR) and Augmented Reality (AR)", "Introduction to Human-Computer Interaction Design",
    "Introduction to Usability Testing", "Introduction to User Experience (UX) Design", "Introduction to Digital Product Management", "Introduction to Agile Software Development",
    "Introduction to Software Engineering", "Introduction to Computer Architecture", "Introduction to Operating Systems", "Introduction to Database Management Systems",
    "Introduction to Computer Networks", "Introduction to Wireless Communication", "Introduction to Mobile App Development", "Introduction to Responsive Web Design", "Introduction to Front-End Web Development",
    "Introduction to Back-End Web Development", "Introduction to Full-Stack Web Development", "Introduction to Cloud-Native Development", "Introduction to Microservices Architecture",
    "Introduction to DevOps Practices", "Introduction to Cybersecurity Operations", "Introduction to Incident Response and Forensics", "Introduction to Security Compliance and Governance",
    "Introduction to Secure Coding Practices", "Introduction to Malware Analysis", "Introduction to Threat Intelligence", "Introduction to Digital Forensics", "Introduction to Security Risk Management",
    "Introduction to Human Factors in Cybersecurity", "Introduction to IT Service Management (ITSM)", "Introduction to ITIL Framework", "Introduction to Cloud Security",
    "Introduction to Blockchain Security", "Introduction to Privacy Engineering", "Introduction to Cybersecurity Law and Ethics", "Introduction to Cybersecurity Policy and Regulation",
    "Introduction to Cybersecurity Standards and Frameworks", "Introduction to Digital Privacy and Data Protection", "Introduction to Cybersecurity Awareness Training", "Introduction to Cybersecurity Risk Assessment",
    "Introduction to Cybersecurity Incident Management", "Introduction to Cybersecurity Strategy and Governance", "Introduction to Cybersecurity Leadership and Management", "Introduction to Cybersecurity Career Pathways",
    "Introduction to Cybersecurity Certifications", "Introduction to Cybersecurity Education and Training", "Introduction to Cybersecurity Research and Development", "Introduction to Cybersecurity Innovation and Entrepreneurship",
    "Introduction to Cybersecurity Collaboration and Community Building", "Introduction to Cybersecurity Advocacy and Policy Making", "Introduction to Cybersecurity Consulting and Advisory Services",
    "Introduction to Cybersecurity Risk Financing and Insurance", "Introduction to Cybersecurity Professional Networking and Mentorship", "Introduction to Cybersecurity Thought Leadership and Public Speaking", "Introduction to Cybersecurity Diversity, Equity, and Inclusion",
    "Introduction to Cybersecurity Nonprofit and Volunteer Work", "Introduction to Cybersecurity Social Media and Online Presence", "Introduction to Cybersecurity Writing and Publishing", "Introduction to Cybersecurity Podcasting and Video Blogging",
    "Introduction to Cybersecurity Conferences and Events", "Introduction to Cybersecurity Communities and Forums", "Introduction to Cybersecurity Webinars and Workshops", "Introduction to Cybersecurity Meetups and Networking Events",
    "Introduction to Cybersecurity Competitions and Hackathons", "Introduction to Cybersecurity Training and Certification Programs", "Introduction to Cybersecurity Degree and Academic Programs", "Introduction to Cybersecurity Bootcamps and Intensive Courses",
    "Introduction to Cybersecurity Mentorship and Coaching Programs", "Introduction to Cybersecurity Internship and Apprenticeship Programs", "Introduction to Cybersecurity Job Fairs and Career Expos", "Introduction to Cybersecurity Job Boards and Recruiting Platforms",
    "Introduction to Cybersecurity Resume Building and Job Search Strategies", "Introduction to Cybersecurity Interview Preparation and Skills", "Introduction to Cybersecurity Professional Development and Continuing Education", "Introduction to Cybersecurity Industry Insights and Trends",
    "Introduction to Cybersecurity Thought Leadership and Influencers", "Introduction to Cybersecurity Professional Associations and Organizations", "Introduction to Cybersecurity Government and Public Sector Careers", "Introduction to Cybersecurity Corporate and Private Sector Careers",
    "Introduction to Cybersecurity Startup and Entrepreneurial Ventures", "Introduction to Cybersecurity Freelance and Consulting Opportunities", "Introduction to Cybersecurity Remote",
    "Introduction to Quantum Computing", "Advanced Data Structures and Algorithms", "Digital Signal Processing Fundamentals", "Introduction to Embedded Systems",
    "Computer Vision and Image Processing", "Advanced Machine Learning Techniques", "Introduction to Natural Language Understanding", "Digital Marketing Strategies",
    "Advanced Financial Accounting", "International Economics and Trade", "Introduction to Game Theory", "Sociology of Globalization", "Advanced Topics in Environmental Science",
    "Neuropsychology: Understanding the Brain and Behavior", "Advanced Topics in Biotechnology", "Cryptocurrency and Blockchain Applications", "Introduction to Cyber Law",
    "Advanced Topics in Network Security", "Big Data Analytics and Visualization", "Introduction to Computational Linguistics", "Augmented Reality Development",
    "Quantum Physics: Theory and Applications", "Introduction to Human-Robot Interaction", "Advanced Topics in Renewable Energy", "Cybersecurity Governance and Compliance",
    "Advanced Topics in Cloud Computing", "Introduction to Bioinformatics", "Advanced Topics in Human-Computer Interaction", "Geopolitics and International Security",
    "Introduction to Health Informatics", "Introduction to String Theory"
]

students = [(i, fake.first_name(), fake.last_name()) for i in range(1, 100001)]
lecturers = [(i, fake.first_name(), fake.last_name()) for i in range(1001, 1051)]
random.shuffle(courses)

# Each course has at least 10 members
Enrol = [[] for _ in range(len(courses))]
for s in students:
    for i in range(3):
        random_course = random.randint(0, len(courses) - 1)
        Enrol[random_course].append(s[0])

# Students do at least 6 courses
for i, students_in_course in enumerate(Enrol):
    if len(students_in_course) > 6:
        Enrol[i] = students_in_course[:6]

# Student in at least 3 courses
for i, students_in_course in enumerate(Enrol):
    while len(students_in_course) < 3:
        random_s = random.randint(0, len(students) - 1)
        sid = students[random_s][0]
        if sid not in students_in_course:
            Enrol[i].append(sid)

# Lecturer only teaches max 5 courses and teaches atleast 1 course
lcourses = [[] for _ in range(len(lecturers))]

for i, lecturer in enumerate(lecturers):
    num_courses = random.randint(1, 5)  
    courses_assigned = random.sample(courses, num_courses) 
    lcourses[i].extend(courses_assigned)

# SQL insert queries
with open('project_data.sql', 'w') as file:
    for student in students:
        email = f"{student[1].lower()}{student[0]}@DBMS.com"
        password = fake.password()
        file.write(f"INSERT INTO User (userID, fname, lname, email, password, role) "
                f"VALUES ({student[0]}, '{student[1]}', '{student[2]}', '{email}', '{password}', 'Student');\n")

    for lecturer in lecturers:
        email = f"{lecturer[1].lower()}{lecturer[0]}@DBMS.com"
        password = fake.password()
        file.write(f"INSERT INTO User (userID, fname, lname, email, password, role) "
                f"VALUES ({lecturer[0]}, '{lecturer[1]}', '{lecturer[2]}', '{email}', '{password}', 'Lecturer');\n")

    for i, course in enumerate(courses):
        file.write(f"INSERT INTO Course (courseID, courseName) VALUES ({i + 1}, '{course}');\n")

    for i, enrol in enumerate(Enrol):
        for student_id in enrol:
            file.write(f"INSERT INTO Enrol (userID, courseID) VALUES ({student_id}, {i + 1});\n")


