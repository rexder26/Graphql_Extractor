import re
import json
import subprocess
import sys

def extract_graphql_components(query):
    
    query_pattern = r'query\s+(\w+)?\s*(\(\$[\w:!,\s]+\))?\{([^}]+)\}'
    matches = re.findall(query_pattern, query)

    components = []
    for match in matches:
        name = match[0]  
        variables = match[1]  
        fields = match[2]  

        
        field_pattern = r'(\w+)(:\w+)?(\{[^}]*\})?'
        field_matches = re.findall(field_pattern, fields)
        field_list = []

        for field_match in field_matches:
            field_name = field_match[0]  
            sub_fields = field_match[2]  

            field_info = {
                'field_name': field_name,
                'sub_fields': []
            }

            if sub_fields:
                
                field_info['sub_fields'] = extract_graphql_components(sub_fields.strip('{}'))

            field_list.append(field_info)

        components.append({
            'query_name': name,
            'variables': variables.strip('()') if variables else None,
            'fields': field_list
        })

    return components

def process_queries(queries):
    all_components = []
    for query in queries:
        components = extract_graphql_components(query)
        all_components.extend(components)
    
    return all_components

def extract_graphql_queries(test_file):
    command = f"grep 'request' {test_file} | cut -d '[' -f3 | cut -d ']' -f1 | sed '1,3d' | base64 -d | grep query | uniq | cut -d '\"' -f4"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip().splitlines()


if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print("Usage: python graphql_extractor.py <path_to_burp_save_file>")
        sys.exit(1)

    test_file_path = sys.argv[1]  

    
    graphql_queries = extract_graphql_queries(test_file_path)

    
    result = process_queries(graphql_queries)

    
    with open('graphql_data.txt', 'w') as output_file:
        json.dump(result, output_file, indent=4)

    print("Extraction complete! Check graphql_data.txt.\n cat graphql_data.txt | jq .")
