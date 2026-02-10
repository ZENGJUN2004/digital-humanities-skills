import pandas as pd
import numpy as np
import json
import yaml
import xml.etree.ElementTree as ET
from datetime import datetime
import os
import re

class HeritageDataManager:
    """
    A comprehensive class for managing cultural heritage data in digital humanities contexts.
    """
    
    def __init__(self, data=None):
        """
        Initialize the HeritageDataManager class with optional data.
        
        Args:
            data (dict or pd.DataFrame, optional): Heritage data to manage.
        """
        self.data = data
    
    def load_data(self, file_path, format='json'):
        """
        Load heritage data from a file.
        
        Args:
            file_path (str): Path to the file containing heritage data.
            format (str): Format of the file ('json', 'yaml', 'csv').
        
        Returns:
            dict or pd.DataFrame: Loaded heritage data.
        """
        try:
            if format == 'json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            elif format == 'yaml':
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.data = yaml.safe_load(f)
            elif format == 'csv':
                self.data = pd.read_csv(file_path)
            else:
                print(f"Unsupported format: {format}")
                return None
            
            print(f"Loaded data from {file_path}")
            return self.data
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def create_metadata(self, artifact_info, standard='dublin_core'):
        """
        Create metadata for a cultural artifact following a specific standard.
        
        Args:
            artifact_info (dict): Information about the artifact.
            standard (str): Metadata standard to use ('dublin_core', 'mods', 'ead').
        
        Returns:
            dict: Created metadata.
        """
        try:
            if standard == 'dublin_core':
                metadata = self._create_dublin_core_metadata(artifact_info)
            elif standard == 'mods':
                metadata = self._create_mods_metadata(artifact_info)
            elif standard == 'ead':
                metadata = self._create_ead_metadata(artifact_info)
            else:
                print(f"Unsupported metadata standard: {standard}")
                return None
            
            print(f"Created {standard} metadata")
            return metadata
        except Exception as e:
            print(f"Error creating metadata: {e}")
            return None
    
    def _create_dublin_core_metadata(self, artifact_info):
        """
        Create Dublin Core metadata for an artifact.
        
        Args:
            artifact_info (dict): Information about the artifact.
        
        Returns:
            dict: Dublin Core metadata.
        """
        metadata = {
            "title": artifact_info.get("title", ""),
            "creator": artifact_info.get("creator", ""),
            "subject": artifact_info.get("subject", ""),
            "description": artifact_info.get("description", ""),
            "publisher": artifact_info.get("publisher", ""),
            "contributor": artifact_info.get("contributor", ""),
            "date": artifact_info.get("date", datetime.now().strftime("%Y-%m-%d")),
            "type": artifact_info.get("type", ""),
            "format": artifact_info.get("format", ""),
            "identifier": artifact_info.get("identifier", ""),
            "source": artifact_info.get("source", ""),
            "language": artifact_info.get("language", ""),
            "relation": artifact_info.get("relation", ""),
            "coverage": artifact_info.get("coverage", ""),
            "rights": artifact_info.get("rights", "")
        }
        return metadata
    
    def _create_mods_metadata(self, artifact_info):
        """
        Create MODS (Metadata Object Description Schema) metadata for an artifact.
        
        Args:
            artifact_info (dict): Information about the artifact.
        
        Returns:
            dict: MODS metadata.
        """
        metadata = {
            "titleInfo": {
                "title": artifact_info.get("title", "")
            },
            "name": {
                "namePart": artifact_info.get("creator", ""),
                "role": {
                    "roleTerm": "creator"
                }
            },
            "subject": {
                "topic": artifact_info.get("subject", "")
            },
            "description": artifact_info.get("description", ""),
            "originInfo": {
                "dateIssued": artifact_info.get("date", datetime.now().strftime("%Y-%m-%d"))
            },
            "typeOfResource": artifact_info.get("type", ""),
            "physicalDescription": {
                "form": artifact_info.get("format", "")
            },
            "identifier": artifact_info.get("identifier", ""),
            "location": {
                "physicalLocation": artifact_info.get("source", "")
            },
            "language": {
                "languageTerm": artifact_info.get("language", "")
            },
            "relatedItem": artifact_info.get("relation", ""),
            "coverage": artifact_info.get("coverage", ""),
            "accessCondition": artifact_info.get("rights", "")
        }
        return metadata
    
    def _create_ead_metadata(self, artifact_info):
        """
        Create EAD (Encoded Archival Description) metadata for an artifact.
        
        Args:
            artifact_info (dict): Information about the artifact.
        
        Returns:
            dict: EAD metadata.
        """
        metadata = {
            "archdesc": {
                "did": {
                    "unittitle": artifact_info.get("title", ""),
                    "unitcreator": artifact_info.get("creator", ""),
                    "unitdate": artifact_info.get("date", datetime.now().strftime("%Y-%m-%d")),
                    "physdesc": {
                        "extent": artifact_info.get("format", "")
                    },
                    "abstract": artifact_info.get("description", ""),
                    "langmaterial": artifact_info.get("language", ""),
                    "note": artifact_info.get("rights", "")
                }
            }
        }
        return metadata
    
    def validate_metadata(self, metadata, standard='dublin_core'):
        """
        Validate metadata against a specific standard.
        
        Args:
            metadata (dict): Metadata to validate.
            standard (str): Metadata standard to use ('dublin_core', 'mods', 'ead').
        
        Returns:
            tuple: (bool, list) - (is_valid, errors)
        """
        try:
            errors = []
            
            if standard == 'dublin_core':
                required_fields = ["title", "creator", "date", "type", "identifier"]
                for field in required_fields:
                    if field not in metadata or not metadata[field]:
                        errors.append(f"Missing required field: {field}")
            
            is_valid = len(errors) == 0
            
            if is_valid:
                print("Metadata validation passed")
            else:
                print("Metadata validation failed")
                for error in errors:
                    print(f"  - {error}")
            
            return is_valid, errors
        except Exception as e:
            print(f"Error validating metadata: {e}")
            return False, [str(e)]
    
    def preservation_planning(self, digital_objects):
        """
        Create a preservation plan for digital objects.
        
        Args:
            digital_objects (list): List of digital objects to preserve.
        
        Returns:
            dict: Preservation plan.
        """
        try:
            plan = {
                "creation_date": datetime.now().strftime("%Y-%m-%d"),
                "digital_objects": [],
                "preservation_actions": []
            }
            
            for obj in digital_objects:
                obj_plan = {
                    "object_id": obj.get("id", ""),
                    "title": obj.get("title", ""),
                    "format": obj.get("format", ""),
                    "size": obj.get("size", ""),
                    "risk_level": self._assess_preservation_risk(obj),
                    "preservation_recommendations": self._generate_preservation_recommendations(obj)
                }
                plan["digital_objects"].append(obj_plan)
            
            # Generate overall preservation actions
            plan["preservation_actions"] = self._generate_preservation_actions(plan["digital_objects"])
            
            print("Created preservation plan")
            return plan
        except Exception as e:
            print(f"Error creating preservation plan: {e}")
            return None
    
    def _assess_preservation_risk(self, digital_object):
        """
        Assess preservation risk for a digital object.
        
        Args:
            digital_object (dict): Digital object to assess.
        
        Returns:
            str: Risk level ('low', 'medium', 'high').
        """
        # Simple risk assessment based on format
        high_risk_formats = ["doc", "xls", "ppt", "wav", "aiff"]
        medium_risk_formats = ["pdf", "jpeg", "png", "mp3", "mp4"]
        low_risk_formats = ["txt", "xml", "json", "csv", "tiff"]
        
        format_ext = digital_object.get("format", "").lower()
        
        if any(fmt in format_ext for fmt in high_risk_formats):
            return "high"
        elif any(fmt in format_ext for fmt in medium_risk_formats):
            return "medium"
        elif any(fmt in format_ext for fmt in low_risk_formats):
            return "low"
        else:
            return "medium"
    
    def _generate_preservation_recommendations(self, digital_object):
        """
        Generate preservation recommendations for a digital object.
        
        Args:
            digital_object (dict): Digital object to generate recommendations for.
        
        Returns:
            list: Preservation recommendations.
        """
        recommendations = []
        risk_level = self._assess_preservation_risk(digital_object)
        
        if risk_level == "high":
            recommendations.append("Migrate to a more stable format")
            recommendations.append("Create multiple copies in different locations")
            recommendations.append("Implement regular integrity checks")
        elif risk_level == "medium":
            recommendations.append("Create backup copies")
            recommendations.append("Monitor format obsolescence")
        else:
            recommendations.append("Maintain regular backups")
        
        recommendations.append("Document object provenance")
        recommendations.append("Store in a controlled environment")
        
        return recommendations
    
    def _generate_preservation_actions(self, digital_objects):
        """
        Generate overall preservation actions based on digital objects.
        
        Args:
            digital_objects (list): List of digital objects.
        
        Returns:
            list: Preservation actions.
        """
        actions = []
        
        # Group objects by risk level
        high_risk_objects = [obj for obj in digital_objects if obj["risk_level"] == "high"]
        medium_risk_objects = [obj for obj in digital_objects if obj["risk_level"] == "medium"]
        
        if high_risk_objects:
            actions.append(f"Prioritize migration of {len(high_risk_objects)} high-risk objects")
        
        if medium_risk_objects:
            actions.append(f"Implement monitoring for {len(medium_risk_objects)} medium-risk objects")
        
        actions.append("Establish regular backup schedule for all objects")
        actions.append("Create preservation metadata for all objects")
        actions.append("Develop disaster recovery plan")
        
        return actions
    
    def organize_collection(self, collection_items):
        """
        Organize a collection of cultural heritage items.
        
        Args:
            collection_items (list): List of collection items.
        
        Returns:
            dict: Organized collection structure.
        """
        try:
            # Organize by type
            organized = {"collections": {}}
            
            for item in collection_items:
                item_type = item.get("type", "Unknown")
                if item_type not in organized["collections"]:
                    organized["collections"][item_type] = []
                organized["collections"][item_type].append(item)
            
            # Add collection metadata
            organized["metadata"] = {
                "total_items": len(collection_items),
                "number_of_collections": len(organized["collections"]),
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            print("Collection organized successfully")
            return organized
        except Exception as e:
            print(f"Error organizing collection: {e}")
            return None
    
    def export_standard_format(self, data, format='json-ld'):
        """
        Export data to a standard format.
        
        Args:
            data (dict or pd.DataFrame): Data to export.
            format (str): Format to export to ('json-ld', 'xml', 'csv').
        
        Returns:
            str or bytes: Exported data.
        """
        try:
            if format == 'json-ld':
                # Add JSON-LD context
                json_ld_data = {
                    "@context": "http://schema.org",
                    **data
                }
                return json.dumps(json_ld_data, indent=2, ensure_ascii=False)
            elif format == 'xml':
                # Convert to XML
                root = ET.Element("heritage_data")
                self._dict_to_xml(root, data)
                return ET.tostring(root, encoding='unicode', xml_declaration=True)
            elif format == 'csv':
                if isinstance(data, pd.DataFrame):
                    return data.to_csv(index=False)
                else:
                    # Convert dict to DataFrame first
                    df = pd.DataFrame(data)
                    return df.to_csv(index=False)
            else:
                print(f"Unsupported export format: {format}")
                return None
        except Exception as e:
            print(f"Error exporting data: {e}")
            return None
    
    def _dict_to_xml(self, parent, data):
        """
        Convert a dictionary to XML.
        
        Args:
            parent (ET.Element): Parent XML element.
            data (dict): Dictionary to convert.
        """
        for key, value in data.items():
            if isinstance(value, dict):
                child = ET.SubElement(parent, key)
                self._dict_to_xml(child, value)
            elif isinstance(value, list):
                for item in value:
                    child = ET.SubElement(parent, key)
                    if isinstance(item, dict):
                        self._dict_to_xml(child, item)
                    else:
                        child.text = str(item)
            else:
                child = ET.SubElement(parent, key)
                child.text = str(value)
    
    def calculate_heritage_value(self, artifact_info):
        """
        Calculate heritage value score for an artifact based on various factors.
        
        Args:
            artifact_info (dict): Information about the artifact.
        
        Returns:
            float: Heritage value score (0-100).
        """
        try:
            score = 0
            
            # Historical significance (30 points)
            if artifact_info.get("historical_significance", ""):
                score += 30
            
            # Cultural significance (25 points)
            if artifact_info.get("cultural_significance", ""):
                score += 25
            
            # Artistic/esthetic value (20 points)
            if artifact_info.get("artistic_value", ""):
                score += 20
            
            # Rarity (15 points)
            if artifact_info.get("rarity", ""):
                score += 15
            
            # Condition (10 points)
            condition = artifact_info.get("condition", "").lower()
            if condition in ["excellent", "good"]:
                score += 10
            elif condition in ["fair"]:
                score += 5
            
            return min(score, 100)
        except Exception as e:
            print(f"Error calculating heritage value: {e}")
            return 0
