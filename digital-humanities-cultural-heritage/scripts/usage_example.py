#!/usr/bin/env python3
"""
Usage example for the HeritageDataManager class in the digital-humanities-cultural-heritage library.
"""

from heritage_data_management import HeritageDataManager
import json

# Sample artifact data generation function
def generate_sample_artifacts():
    """
    Generate sample artifact data for testing.
    
    Returns:
        list: Sample artifact data.
    """
    artifacts = [
        {
            "id": "art001",
            "title": "Ancient Manuscript",
            "creator": "Unknown Monk",
            "date": "1200-01-01",
            "type": "Manuscript",
            "format": "Handwritten parchment",
            "identifier": "MS-001",
            "source": "Medieval Library",
            "language": "Latin",
            "description": "A medieval manuscript containing religious texts",
            "historical_significance": "Important for understanding medieval religious practices",
            "cultural_significance": "Represents the cultural heritage of medieval Europe",
            "artistic_value": "Contains beautiful illuminations",
            "rarity": "Rare example of 13th-century manuscript",
            "condition": "Good"
        },
        {
            "id": "art002",
            "title": "Ceramic Vase",
            "creator": "Ancient Potter",
            "date": "500 BCE",
            "type": "Ceramic",
            "format": "Hand-thrown pottery",
            "identifier": "CER-002",
            "source": "Archaeological Excavation",
            "language": "N/A",
            "description": "An ancient ceramic vase with geometric patterns",
            "historical_significance": "Provides insight into ancient pottery techniques",
            "cultural_significance": "Represents the artistic traditions of the period",
            "artistic_value": "Exhibits skilled craftsmanship",
            "rarity": "Common type of artifact from this period",
            "condition": "Fair"
        },
        {
            "id": "art003",
            "title": "Digital Artwork",
            "creator": "Contemporary Artist",
            "date": "2023-01-01",
            "type": "Digital Art",
            "format": "JPEG image",
            "identifier": "DIG-003",
            "source": "Artist's Portfolio",
            "language": "N/A",
            "description": "A digital artwork exploring cultural identity",
            "historical_significance": "Represents contemporary digital art practices",
            "cultural_significance": "Explores themes of cultural identity in the digital age",
            "artistic_value": "Innovative use of digital techniques",
            "rarity": "Unique digital artwork",
            "condition": "Excellent"
        }
    ]
    return artifacts

# Sample digital objects for preservation planning
def generate_sample_digital_objects():
    """
    Generate sample digital objects for preservation planning.
    
    Returns:
        list: Sample digital objects.
    """
    digital_objects = [
        {
            "id": "dig001",
            "title": "High-Resolution Manuscript Scan",
            "format": "TIFF",
            "size": "100 MB",
            "creation_date": "2020-01-01"
        },
        {
            "id": "dig002",
            "title": "Oral History Interview",
            "format": "WAV",
            "size": "500 MB",
            "creation_date": "2019-06-15"
        },
        {
            "id": "dig003",
            "title": "Interactive Exhibition",
            "format": "HTML5/JavaScript",
            "size": "2 GB",
            "creation_date": "2022-03-10"
        },
        {
            "id": "dig004",
            "title": "3D Model of Archaeological Site",
            "format": "OBJ",
            "size": "1.5 GB",
            "creation_date": "2021-11-20"
        }
    ]
    return digital_objects

def main():
    """
    Main function to demonstrate the HeritageDataManager class.
    """
    print("=== Digital Humanities Cultural Heritage Management ===")
    
    # Create HeritageDataManager instance
    hdm = HeritageDataManager()
    
    # Generate sample artifacts
    print("Creating sample artifacts...")
    artifacts = generate_sample_artifacts()
    print(f"Generated {len(artifacts)} sample artifacts")
    
    # 1. Create metadata for artifacts
    print("\n1. Creating metadata for artifacts...")
    for artifact in artifacts:
        print(f"\nCreating metadata for: {artifact['title']}")
        
        # Create Dublin Core metadata
        dc_metadata = hdm.create_metadata(artifact, standard='dublin_core')
        print("Dublin Core metadata created")
        
        # Validate metadata
        is_valid, errors = hdm.validate_metadata(dc_metadata, standard='dublin_core')
        
        # Create MODS metadata
        mods_metadata = hdm.create_metadata(artifact, standard='mods')
        print("MODS metadata created")
    
    # 2. Calculate heritage value
    print("\n2. Calculating heritage value...")
    for artifact in artifacts:
        value = hdm.calculate_heritage_value(artifact)
        print(f"{artifact['title']}: Heritage value score = {value}/100")
    
    # 3. Create preservation plan
    print("\n3. Creating preservation plan...")
    digital_objects = generate_sample_digital_objects()
    preservation_plan = hdm.preservation_planning(digital_objects)
    print(f"Created preservation plan for {len(preservation_plan['digital_objects'])} digital objects")
    print("Preservation actions:")
    for action in preservation_plan['preservation_actions']:
        print(f"  - {action}")
    
    # 4. Organize collection
    print("\n4. Organizing collection...")
    organized_collection = hdm.organize_collection(artifacts)
    print(f"Organized collection into {organized_collection['metadata']['number_of_collections']} categories")
    print("Collection categories:")
    for category, items in organized_collection['collections'].items():
        print(f"  - {category}: {len(items)} items")
    
    # 5. Export data
    print("\n5. Exporting data...")
    # Export as JSON-LD
    json_ld_output = hdm.export_standard_format(artifacts[0], format='json-ld')
    print("Exported artifact metadata as JSON-LD")
    
    # Export as XML
    xml_output = hdm.export_standard_format(artifacts[0], format='xml')
    print("Exported artifact metadata as XML")
    
    print("\n=== Heritage Management Demonstration Complete ===")

if __name__ == "__main__":
    main()
