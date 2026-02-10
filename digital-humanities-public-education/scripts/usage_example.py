#!/usr/bin/env python3
"""
Usage example for the EducationalContentManager class in the digital-humanities-public-education library.
"""

from educational_content_manager import EducationalContentManager
import json

# Sample course data generation function
def generate_sample_course():
    """
    Generate sample course data for testing.
    
    Returns:
        dict: Sample course data.
    """
    return {
        "title": "Introduction to Digital Humanities",
        "description": "This course introduces students to the field of digital humanities, exploring how digital tools and methods can enhance humanities research and education.",
        "instructor": "Dr. Digital Humanist",
        "level": "Beginner",
        "duration": "10 weeks",
        "learning_objectives": [
            "Understand the fundamental concepts of digital humanities",
            "Learn to use digital tools for humanities research",
            "Develop critical thinking about digital methods in humanities",
            "Create a digital humanities project"
        ],
        "modules": [
            {
                "title": "What is Digital Humanities?",
                "description": "An introduction to the field and its history",
                "activities": [
                    "Read foundational texts",
                    "Discuss key debates",
                    "Explore digital humanities projects"
                ]
            },
            {
                "title": "Digital Tools for Research",
                "description": "Introduction to digital tools for humanities research",
                "activities": [
                    "Learn text analysis techniques",
                    "Explore data visualization",
                    "Practice digital mapping"
                ]
            },
            {
                "title": "Digital Project Design",
                "description": "Designing and planning a digital humanities project",
                "activities": [
                    "Develop project proposals",
                    "Create project timelines",
                    "Identify resources and tools"
                ]
            },
            {
                "title": "Project Implementation",
                "description": "Implementing a digital humanities project",
                "activities": [
                    "Collect and prepare data",
                    "Use digital tools for analysis",
                    "Create project outputs"
                ]
            },
            {
                "title": "Project Presentation",
                "description": "Presenting digital humanities projects",
                "activities": [
                    "Prepare project presentations",
                    "Receive peer feedback",
                    "Revise projects"
                ]
            }
        ],
        "resources": [
            {"title": "Digital Humanities Reader", "type": "Book"},
            {"title": "Programming Historian", "type": "Website"},
            {"title": "DH Commons", "type": "Online Community"},
            {"title": "Text Analysis with Python", "type": "Tutorial"}
        ],
        "assessment_strategy": "Project-based assessment with peer review"
    }

# Sample digital story data generation function
def generate_sample_digital_story():
    """
    Generate sample digital story data for testing.
    
    Returns:
        dict: Sample digital story data.
    """
    return {
        "title": "The Digital Evolution of Literature",
        "author": "Digital Storyteller",
        "topic": "Literary History",
        "narrative": "This digital story explores how literature has evolved in the digital age, from early electronic texts to interactive narratives and beyond.",
        "media_elements": [
            {"type": "Image", "description": "Early electronic text interface"},
            {"type": "Video", "description": "Interview with digital author"},
            {"type": "Audio", "description": "Podcast discussion of digital literature"},
            {"type": "Interactive", "description": "Digital narrative example"}
        ],
        "interactive_elements": [
            {"type": "Quiz", "description": "Literary digital evolution quiz"},
            {"type": "Timeline", "description": "Interactive timeline of digital literature"},
            {"type": "Gallery", "description": "Digital literature examples"}
        ],
        "learning_outcomes": [
            "Understand the evolution of digital literature",
            "Analyze digital narrative techniques",
            "Evaluate the impact of digital tools on literary creation"
        ],
        "target_audience": "Undergraduate literature students"
    }

# Sample community project data generation function
def generate_sample_community_project():
    """
    Generate sample community project data for testing.
    
    Returns:
        dict: Sample community project data.
    """
    return {
        "title": "Local History Digital Archive",
        "description": "A community-based project to digitize and preserve local history materials, making them accessible to the public.",
        "community_partners": [
            "Local Historical Society",
            "Public Library",
            "Community College",
            "City Government"
        ],
        "goals": [
            "Digitize 500 local history documents",
            "Create an online archive accessible to the public",
            "Develop educational resources based on archive materials",
            "Engage community members in local history preservation"
        ],
        "activities": [
            "Organize digitization workshops",
            "Train community volunteers",
            "Develop archive metadata schema",
            "Create educational lesson plans",
            "Host public events showcasing the archive"
        ],
        "timeline": "12-month project: 3 months planning, 6 months digitization, 3 months outreach and education",
        "resources": [
            {"title": "Digitization equipment", "type": "Hardware"},
            {"title": "Archive software", "type": "Software"},
            {"title": "Community space", "type": "Venue"},
            {"title": "Volunteer time", "type": "Human Resource"}
        ],
        "evaluation_plan": "Measure success through number of items digitized, website traffic, educational resources created, and community engagement metrics",
        "contact_information": "localhistoryarchive@example.com"
    }

# Sample learning resources data generation function
def generate_sample_learning_resources():
    """
    Generate sample learning resources for testing.
    
    Returns:
        list: Sample learning resources.
    """
    return [
        {
            "id": "res001",
            "title": "Text Mining for Humanists",
            "type": "Tutorial",
            "topic": "Text Analysis",
            "level": "Intermediate",
            "description": "A step-by-step guide to text mining for humanities research"
        },
        {
            "id": "res002",
            "title": "Introduction to Python",
            "type": "Course",
            "topic": "Programming",
            "level": "Beginner",
            "description": "An introductory Python course for humanities students"
        },
        {
            "id": "res003",
            "title": "Digital Mapping Tools",
            "type": "Workshop",
            "topic": "Spatial Analysis",
            "level": "Intermediate",
            "description": "Hands-on workshop on digital mapping for historical research"
        },
        {
            "id": "res004",
            "title": "Digital Humanities Ethics",
            "type": "Lecture",
            "topic": "Ethics",
            "level": "Advanced",
            "description": "Exploration of ethical issues in digital humanities research"
        },
        {
            "id": "res005",
            "title": "Data Visualization for Humanities",
            "type": "Guide",
            "topic": "Visualization",
            "level": "Intermediate",
            "description": "Best practices for visualizing humanities data"
        }
    ]

# Sample lesson plan data generation function
def generate_sample_lesson_plan():
    """
    Generate sample lesson plan data for testing.
    
    Returns:
        dict: Sample lesson plan data.
    """
    return {
        "title": "Introduction to Text Analysis",
        "subject": "Digital Humanities",
        "duration": "90 minutes",
        "learning_objectives": [
            "Understand the basics of text analysis",
            "Learn to use text analysis tools",
            "Apply text analysis to a literary text"
        ],
        "prerequisites": [
            "Basic computer literacy",
            "Familiarity with literary analysis"
        ],
        "materials": [
            "Computers with internet access",
            "Text analysis software",
            "Sample literary texts",
            "Worksheets"
        ],
        "procedure": [
            "Introduction to text analysis (15 minutes)",
            "Demonstration of text analysis tools (20 minutes)",
            "Guided practice with sample texts (30 minutes)",
            "Independent exploration (15 minutes)",
            "Discussion and reflection (10 minutes)"
        ],
        "assessment": "Students will submit a short analysis of their text using text analysis tools",
        "differentiation": "Provide additional support for students new to digital tools; offer advanced challenges for students with technical experience",
        "extension_activities": [
            "Apply text analysis to a text of student's choice",
            "Research different text analysis techniques",
            "Create a visualization of text analysis results"
        ],
        "resources": [
            {"title": "Text Analysis Toolkit", "type": "Software"},
            {"title": "Introduction to Text Analysis", "type": "Article"},
            {"title": "Text Analysis Examples", "type": "Website"}
        ]
    }

# Sample impact data generation function
def generate_sample_impact_data():
    """
    Generate sample impact data for testing.
    
    Returns:
        dict: Sample impact data.
    """
    return {
        "project_name": "Local History Digital Archive",
        "evaluation_type": "Educational Impact",
        "data_collection_methods": ["Survey", "Interview", "Website Analytics", "Project Documentation"],
        "participant_data": [
            {"role": "Student", "count": 50},
            {"role": "Community Member", "count": 30},
            {"role": "Educator", "count": 10}
        ],
        "learning_outcomes_achieved": [
            {"outcome": "Increased digital literacy", "achieved": True},
            {"outcome": "Improved understanding of local history", "achieved": True},
            {"outcome": "Developed digital preservation skills", "achieved": True},
            {"outcome": "Created digital humanities projects", "achieved": False}
        ],
        "engagement_metrics": {
            "participation_rate": 85,
            "completion_rate": 70,
            "satisfaction_score": 4.5
        },
        "qualitative_feedback": [
            {"feedback": "This project helped me understand my local history better", "sentiment": "positive"},
            {"feedback": "The digital skills I learned were valuable", "sentiment": "positive"},
            {"feedback": "More time for project development would be helpful", "sentiment": "neutral"}
        ],
        "recommendations": [
            {"recommendation": "Expand the archive to include more recent history", "implemented": False},
            {"recommendation": "Develop more educational resources", "implemented": True},
            {"recommendation": "Offer more workshops on digital tools", "implemented": True}
        ]
    }

def main():
    """
    Main function to demonstrate the EducationalContentManager class.
    """
    print("=== Digital Humanities Public Education Management ===")
    
    # Create EducationalContentManager instance
    ecm = EducationalContentManager()
    
    # 1. Create a course
    print("\n1. Creating a digital humanities course...")
    course_data = generate_sample_course()
    course = ecm.create_course(course_data)
    print(f"Course created: {course['title']}")
    print(f"Number of modules: {len(course['modules'])}")
    
    # 2. Create a digital story
    print("\n2. Creating a digital story...")
    story_data = generate_sample_digital_story()
    story = ecm.create_digital_story(story_data)
    print(f"Digital story created: {story['title']}")
    print(f"Number of media elements: {len(story['media_elements'])}")
    
    # 3. Create a community project
    print("\n3. Creating a community project...")
    project_data = generate_sample_community_project()
    project = ecm.create_community_project(project_data)
    print(f"Community project created: {project['title']}")
    print(f"Number of community partners: {len(project['community_partners'])}")
    
    # 4. Organize learning resources
    print("\n4. Organizing learning resources...")
    resources = generate_sample_learning_resources()
    organized_resources = ecm.organize_learning_resources(resources)
    print(f"Organized {organized_resources['metadata']['total_resources']} resources")
    print(f"Resources by type: {list(organized_resources['by_type'].keys())}")
    print(f"Resources by topic: {list(organized_resources['by_topic'].keys())}")
    
    # 5. Generate a lesson plan
    print("\n5. Generating a lesson plan...")
    lesson_data = generate_sample_lesson_plan()
    lesson_plan = ecm.generate_lesson_plan(lesson_data)
    print(f"Lesson plan generated: {lesson_plan['title']}")
    print(f"Duration: {lesson_plan['duration']}")
    
    # 6. Evaluate educational impact
    print("\n6. Evaluating educational impact...")
    impact_data = generate_sample_impact_data()
    impact_evaluation = ecm.evaluate_educational_impact(impact_data)
    print(f"Impact evaluation completed for: {impact_evaluation['project_name']}")
    print(f"Overall impact score: {impact_evaluation['overall_impact_score']}/100")
    
    # 7. Export content
    print("\n7. Exporting content...")
    # Export course as markdown
    md_course = ecm.export_content(course, format='markdown')
    print("Course exported as Markdown")
    
    # Export lesson plan as JSON
    json_lesson = ecm.export_content(lesson_plan, format='json')
    print("Lesson plan exported as JSON")
    
    # 8. Create accessibility report
    print("\n8. Creating accessibility report...")
    accessibility_report = ecm.create_accessibility_report(course)
    print(f"Accessibility report created for: {accessibility_report['content_title']}")
    print(f"Compliance score: {accessibility_report['compliance_score']}/100")
    
    print("\n=== Education Management Demonstration Complete ===")

if __name__ == "__main__":
    main()
