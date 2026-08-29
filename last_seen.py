import json
def write_last_seen(last_seen):
    with open("state.json",'w') as l:
        json.dump(last_seen,l)
    print(last_seen)
        

def read_last_seen():
    try:
        with open("state.json",'r') as l:
             ll=json.load(l)
             return ll

    except (FileNotFoundError,json.JSONDecodeError):
            return None

    
    