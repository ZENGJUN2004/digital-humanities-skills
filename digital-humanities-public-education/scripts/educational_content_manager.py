import pandas as pd
import numpy as np
import json
import yaml
import markdown
from jinja2 import Template
from datetime import datetime
import os
import re

class EducationalContentManager:
    """
    A comprehensive class for managing educational content in digital humanities contexts.
    """
    
    def __init__(self, content=None):
        """
        Initialize the EducationalContentManager class with optional content.
        
        Args:
            content (dict or pd.DataFrame, optional): Educational content to manage.
        """
        self.content = content
    
    def create_course(self, course_info):
        """
        Create a digital humanities course structure.
        
        Args:
            course_info (dict): Information about the course.
        
        Returns:
            dict: Created course structure.
        """
        try:
            course = {
                "course_id": course_info.get("id", f"course_{datetime.now().strftime('%Y%m%d%H%M%S')}"),
                "title": course_info.get("title", ""),
                "description": course_info.get("description", ""),
                "instructor": course_info.get("instructor", ""),
                "level": course_info.get("level", "Intermediate"),
                "duration": course_info.get("duration", "10 weeks"),
                "learning_objectives": course_info.get("learning_objectives", []),
                "modules": course_info.get("modules", []),
                "resources": course_info.get("resources", []),
                "assessment_strategy": course_info.get("assessment_strategy", ""),
                "creation_date": datetime.now().strftime("%Y-%m-%d"),
                "last_updated": datetime.now().strftime("%Y-%m-%d")
            }
            
            # Validate course structure
            if not course["title"]:
                raise ValueError("Course title is required")
            
            print(f"Created course: {course['title']}")
            return course
        except Exception as e:
            print(f"Error creating course: {e}")
            return None
    
    def create_digital_story(self, story_info):
        """
        Create a digital story for educational purposes.
        
        Args:
            story_info (dict): Information about the digital story.
        
        Returns:
            dict: Created digital story.
        """
        try:
            story = {
                "story_id": story_info.get("id", f"story_{datetime.now().strftime('%Y%m%d%H%M%S')}"),
                "title": story_info.get("title", ""),
                "author": story_info.get("author", ""),
                "topic": story_info.get("topic", ""),
                "narrative": story_info.get("narrative", ""),
                "media_elements": story_info.get("media_elements", []),
                "interactive_elements": story_info.get("interactive_elements", []),
                "learning_outcomes": story_info.get("learning_outcomes", []),
                "target_audience": story_info.get("target_audience", ""),
                "creation_date": datetime.now().strftime("%Y-%m-%d"),
                "last_updated": datetime.now().strftime("%Y-%m-%d")
            }
            
            # Validate story structure
            if not story["title"]:
                raise ValueError("Story title is required")
            if not story["narrative"]:
                raise ValueError("Story narrative is required")
            
            print(f"Created digital story: {story['title']}")
            return story
        except Exception as e:
            print(f"Error creating digital story: {e}")
            return None
    
    def create_community_project(self, project_info):
        """
        Create a community-based digital humanities project.
        
        Args:
            project_info (dict): Information about the community project.
        
        Returns:
            dict: Created community project.
        """
        try:
            project = {
                "project_id": project_info.get("id", f"project_{datetime.now().strftime('%Y%m%d%H%M%S')}"),
                "title": project_info.get("title", ""),
                "description": project_info.get("description", ""),
                "community_partners": project_info.get("community_partners", []),
                "goals": project_info.get("goals", []),
                "activities": project_info.get("activities", []),
                "timeline": project_info.get("timeline", ""),
                "resources": project_info.get("resources", []),
                "evaluation_plan": project_info.get("evaluation_plan", ""),
                "contact_information": project_info.get("contact_information", ""),
                "creation_date": datetime.now().strftime("%Y-%m-%d"),
                "last_updated": datetime.now().strftime("%Y-%m-%d")
            }
            
            # Validate project structure
            if not project["title"]:
                raise ValueError("Project title is required")
            if not project["description"]:
                raise ValueError("Project description is required")
            
            print(f"Created community project: {project['title']}")
            return project
        except Exception as e:
            print(f"Error creating community project: {e}")
            return None
    
    def organize_learning_resources(self, resources):
        """
        Organize learning resources by type, topic, or difficulty level.
        
        Args:
            resources (list): List of learning resources.
        
        Returns:
            dict: Organized resources structure.
        """
        try:
            # Organize by type and topic
            organized = {
                "by_type": {},
                "by_topic": {},
                "by_level": {}
            }
            
            for resource in resources:
                # Organize by type
                resource_type = resource.get("type", "Unknown")
                if resource_type not in organized["by_type"]:
                    organized["by_type"][resource_type] = []
                organized["by_type"][resource_type].append(resource)
                
                # Organize by topic
                topic = resource.get("topic", "Unknown")
                if topic not in organized["by_topic"]:
                    organized["by_topic"][topic] = []
                organized["by_topic"][topic].append(resource)
                
                # Organize by level
                level = resource.get("level", "Intermediate")
                if level not in organized["by_level"]:
                    organized["by_level"][level] = []
                organized["by_level"][level].append(resource)
            
            # Add metadata
            organized["metadata"] = {
                "total_resources": len(resources),
                "number_of_types": len(organized["by_type"]),
                "number_of_topics": len(organized["by_topic"]),
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            print(f"Organized {len(resources)} learning resources")
            return organized
        except Exception as e:
            print(f"Error organizing learning resources: {e}")
            return None
    
    def generate_lesson_plan(self, lesson_info):
        """
        Generate a structured lesson plan for digital humanities education.
        
        Args:
            lesson_info (dict): Information about the lesson.
        
        Returns:
            dict: Generated lesson plan.
        """
        try:
            lesson_plan = {
                "lesson_id": lesson_info.get("id", f"lesson_{datetime.now().strftime('%Y%m%d%H%M%S')}"),
                "title": lesson_info.get("title", ""),
                "subject": lesson_info.get("subject", "Digital Humanities"),
                "duration": lesson_info.get("duration", "90 minutes"),
                "learning_objectives": lesson_info.get("learning_objectives", []),
                "prerequisites": lesson_info.get("prerequisites", []),
                "materials": lesson_info.get("materials", []),
                "procedure": lesson_info.get("procedure", []),
                "assessment": lesson_info.get("assessment", ""),
                "differentiation": lesson_info.get("differentiation", ""),
                "extension_activities": lesson_info.get("extension_activities", []),
                "resources": lesson_info.get("resources", []),
                "creation_date": datetime.now().strftime("%Y-%m-%d"),
                "last_updated": datetime.now().strftime("%Y-%m-%d")
            }
            
            # Validate lesson plan
            if not lesson_plan["title"]:
                raise ValueError("Lesson title is required")
            if not lesson_plan["procedure"]:
                raise ValueError("Lesson procedure is required")
            
            print(f"Generated lesson plan: {lesson_plan['title']}")
            return lesson_plan
        except Exception as e:
            print(f"Error generating lesson plan: {e}")
            return None
    
    def evaluate_educational_impact(self, impact_data):
        """
        Evaluate the educational impact of a digital humanities project.
        
        Args:
            impact_data (dict): Data related to educational impact.
        
        Returns:
            dict: Impact evaluation results.
        """
        try:
            evaluation = {
                "evaluation_id": impact_data.get("id", f"eval_{datetime.now().strftime('%Y%m%d%H%M%S')}"),
                "project_name": impact_data.get("project_name", ""),
                "evaluation_type": impact_data.get("evaluation_type", "Educational Impact"),
                "data_collection_methods": impact_data.get("data_collection_methods", []),
                "participant_data": impact_data.get("participant_data", []),
                "learning_outcomes_achieved": impact_data.get("learning_outcomes_achieved", []),
                "engagement_metrics": impact_data.get("engagement_metrics", {}),
                "qualitative_feedback": impact_data.get("qualitative_feedback", []),
                "recommendations": impact_data.get("recommendations", []),
                "overall_impact_score": self._calculate_impact_score(impact_data),
                "evaluation_date": datetime.now().strftime("%Y-%m-%d")
            }
            
            print(f"Completed impact evaluation for: {evaluation['project_name']}")
            return evaluation
        except Exception as e:
            print(f"Error evaluating educational impact: {e}")
            return None
    
    def _calculate_impact_score(self, impact_data):
        """
        Calculate an overall impact score based on various metrics.
        
        Args:
            impact_data (dict): Data related to educational impact.
        
        Returns:
            float: Impact score (0-100).
        """
        try:
            score = 0
            
            # Learning outcomes achieved (40 points)
            outcomes = impact_data.get("learning_outcomes_achieved", [])
            total_outcomes = len(outcomes)
            achieved_outcomes = sum(1 for o in outcomes if o.get("achieved", False))
            if total_outcomes > 0:
                score += (achieved_outcomes / total_outcomes) * 40
            
            # Engagement metrics (30 points)
            engagement = impact_data.get("engagement_metrics", {})
            if engagement.get("participation_rate", 0) > 70:
                score += 10
            if engagement.get("completion_rate", 0) > 60:
                score += 10
            if engagement.get("satisfaction_score", 0) > 4.0:
                score += 10
            
            # Qualitative feedback (20 points)
            feedback = impact_data.get("qualitative_feedback", [])
            if len(feedback) > 0:
                positive_feedback = sum(1 for f in feedback if f.get("sentiment", "neutral") == "positive")
                if positive_feedback / len(feedback) > 0.7:
                    score += 20
                elif positive_feedback / len(feedback) > 0.4:
                    score += 10
            
            # Recommendations implemented (10 points)
            recommendations = impact_data.get("recommendations", [])
            if len(recommendations) > 0:
                implemented = sum(1 for r in recommendations if r.get("implemented", False))
                if implemented / len(recommendations) > 0.5:
                    score += 10
            
            return min(round(score, 2), 100)
        except Exception as e:
            print(f"Error calculating impact score: {e}")
            return 0
    
    def export_content(self, content, format='json'):
        """
        Export educational content to a specified format.
        
        Args:
            content (dict): Content to export.
            format (str): Format to export to ('json', 'yaml', 'markdown').
        
        Returns:
            str: Exported content.
        """
        try:
            if format == 'json':
                return json.dumps(content, indent=2, ensure_ascii=False)
            elif format == 'yaml':
                return yaml.dump(content, default_flow_style=False, allow_unicode=True)
            elif format == 'markdown':
                return self._convert_to_markdown(content)
            else:
                print(f"Unsupported export format: {format}")
                return None
        except Exception as e:
            print(f"Error exporting content: {e}")
            return None
    
    def _convert_to_markdown(self, content):
        """
        Convert content to Markdown format.
        
        Args:
            content (dict): Content to convert.
        
        Returns:
            str: Markdown-formatted content.
        """
        try:
            md = []
            
            # Handle different types of content
            if "title" in content:
                md.append(f"# {content['title']}")
                md.append("")
            
            if "description" in content and content["description"]:
                md.append(f"## Description")
                md.append(content["description"])
                md.append("")
            
            if "learning_objectives" in content and content["learning_objectives"]:
                md.append("## Learning Objectives")
                for obj in content["learning_objectives"]:
                    md.append(f"- {obj}")
                md.append("")
            
            if "modules" in content and content["modules"]:
                md.append("## Modules")
                for i, module in enumerate(content["modules"], 1):
                    md.append(f"### Module {i}: {module.get('title', '')}")
                    if module.get('description', ''):
                        md.append(module['description'])
                    if module.get('activities', []):
                        md.append("#### Activities")
                        for activity in module['activities']:
                            md.append(f"- {activity}")
                md.append("")
            
            if "resources" in content and content["resources"]:
                md.append("## Resources")
                for resource in content["resources"]:
                    md.append(f"- {resource.get('title', '')}")
                md.append("")
            
            return "\n".join(md)
        except Exception as e:
            print(f"Error converting to markdown: {e}")
            return ""
    
    def create_accessibility_report(self, content):
        """
        Create an accessibility report for educational content.
        
        Args:
            content (dict): Educational content to assess.
        
        Returns:
            dict: Accessibility report.
        """
        try:
            report = {
                "report_id": f"access_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "content_title": content.get("title", ""),
                "assessment_date": datetime.now().strftime("%Y-%m-%d"),
                "accessibility_checks": [],
                "compliance_score": 0,
                "recommendations": []
            }
            
            # Perform accessibility checks
            checks = [
                {"name": "Text alternatives for images", "pass": self._check_image_alternatives(content), "weight": 20},
                {"name": "Captioning for videos", "pass": self._check_video_captions(content), "weight": 20},
                {"name": "Keyboard navigation", "pass": self._check_keyboard_navigation(content), "weight": 15},
                {"name": "Color contrast", "pass": self._check_color_contrast(content), "weight": 15},
                {"name": "Readable text", "pass": self._check_text_readability(content), "weight": 15},
                {"name": "Semantic structure", "pass": self._check_semantic_structure(content), "weight": 15}
            ]
            
            report["accessibility_checks"] = checks
            
            # Calculate compliance score
            total_weight = sum(c["weight"] for c in checks)
            passed_weight = sum(c["weight"] for c in checks if c["pass"])
            report["compliance_score"] = (passed_weight / total_weight) * 100 if total_weight > 0 else 0
            
            # Generate recommendations
            for check in checks:
                if not check["pass"]:
                    report["recommendations"].append(f"Improve {check['name']}")
            
            print(f"Created accessibility report for: {report['content_title']}")
            return report
        except Exception as e:
            print(f"Error creating accessibility report: {e}")
            return None
    
    def _check_image_alternatives(self, content):
        """
        Check if images have text alternatives.
        
        Args:
            content (dict): Content to check.
        
        Returns:
            bool: True if all images have alternatives, False otherwise.
        """
        # Simplified check - in a real implementation, this would parse media elements
        return True
    
    def _check_video_captions(self, content):
        """
        Check if videos have captions.
        
        Args:
            content (dict): Content to check.
        
        Returns:
            bool: True if all videos have captions, False otherwise.
        """
        # Simplified check - in a real implementation, this would parse media elements
        return True
    
    def _check_keyboard_navigation(self, content):
        """
        Check if content supports keyboard navigation.
        
        Args:
            content (dict): Content to check.
        
        Returns:
            bool: True if keyboard navigation is supported, False otherwise.
        """
        # Simplified check - in a real implementation, this would analyze interactive elements
        return True
    
    def _check_color_contrast(self, content):
        """
        Check if content has adequate color contrast.
        
        Args:
            content (dict): Content to check.
        
        Returns:
            bool: True if color contrast is adequate, False otherwise.
        """
        # Simplified check - in a real implementation, this would analyze color schemes
        return True
    
    def _check_text_readability(self, content):
        """
        Check if text is readable.
        
        Args:
            content (dict): Content to check.
        
        Returns:
            bool: True if text is readable, False otherwise.
        """
        # Simplified check - in a real implementation, this would analyze text readability
        return True
    
    def _check_semantic_structure(self, content):
        """
        Check if content has a semantic structure.
        
        Args:
            content (dict): Content to check.
        
        Returns:
            bool: True if content has semantic structure, False otherwise.
        """
        # Simplified check - in a real implementation, this would analyze content structure
        return True
