import json
import base64
import requests
import time
from datetime import datetime

NOTE_FILE = "note2self.json"

def read_note():
    try:
        with open(NOTE_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # Create a new note if the file is not found
        new_note = {"timestamp": None, "improvement": {}, "assessment": ""}
        write_note(new_note)
        return new_note
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON from note file: {e}")
        return {"timestamp": None, "improvement": {}, "assessment": ""}

def write_note(note):
    with open(NOTE_FILE, 'w') as file:
        json.dump(note, file)

def call_github_copilot(note):
    query = "This is a summary of last cycle events. Please can you help me take a look at the repo so we can identify an item for the next incremental improvement?"
    payload = {"note": note, "query": query}
    content = base64.b64encode(json.dumps(payload).encode()).decode()
    
    url = "https://api.github.com/repos/EchoCog/echosurface/contents/.github/workflows/request_payload.json"
    headers = {
        "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
        "Content-Type": "application/json"
    }
    data = {
        "message": "Add request payload",
        "content": content,
        "branch": "main"
    }
    
    response = requests.put(url, headers=headers, json=data)
    
    try:
        if response.headers.get('Content-Type') == 'application/json':
            return response.json()
        else:
            print(f"Unexpected content type: {response.headers.get('Content-Type')}")
            print(f"Response content: {response.text}")
            return None
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        return None

def introspect_repo():
    introspection_result = {
        "errors": ["example_error_1", "example_error_2"],
        "problem_areas": ["example_problem_area_1", "example_problem_area_2"]
    }
    return introspection_result

def apply_improvement(improvement):
    print(f"Applying improvement: {improvement}")

def run_workflow():
    result = "success"
    return result

def main():
    max_retries = 3
    retries = 0

    previous_note = read_note()

    introspection_result = introspect_repo()

    copilot_response = call_github_copilot(previous_note)

    if copilot_response is None:
        print("Failed to get a valid response from GitHub Copilot.")
        return

    improvement = copilot_response.get("improvement")
    assessment = copilot_response.get("assessment")

    apply_improvement(improvement)

    while retries < max_retries:
        result = run_workflow()
        if result == "success":
            break
        else:
            retries += 1
            time.sleep(10)

    new_note = {
        "timestamp": datetime.utcnow().isoformat(),
        "improvement": improvement,
        "assessment": assessment,
        "result": result,
        "retries": retries
    }
    write_note(new_note)

    print(f"Self-improvement cycle complete. Result: {result}, Assessment: {assessment}")

if __name__ == "__main__":
    main()
