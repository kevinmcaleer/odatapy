from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import yaml
import os

app = FastAPI()

# Directory where YAML files are stored
YAML_DIR = "path/to/your/yaml/files"

def load_yaml_data():
    data = {}
    for filename in os.listdir(YAML_DIR):
        if filename.endswith(".yml") or filename.endswith(".yaml"):
            with open(os.path.join(YAML_DIR, filename), "r") as f:
                file_data = yaml.safe_load(f)
                # Use filename (without extension) as the key for each dataset
                data[os.path.splitext(filename)[0]] = file_data
    return data

@app.get("/odata/{entity}")
async def get_entity_data(entity: str):
    # Load the YAML data
    data = load_yaml_data()
    
    # Check if the entity exists in loaded data
    if entity not in data:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    # Structure response as OData with basic metadata
    response = {
        "@odata.context": f"/odata/{entity}",
        "value": data[entity]
    }
    
    return JSONResponse(content=response)

@app.get("/odata/")
async def get_entities():
    # Get all available entities (keys from YAML files)
    data = load_yaml_data()
    entities = [{"name": name, "@odata.id": f"/odata/{name}"} for name in data.keys()]
    
    response = {
        "@odata.context": "/odata",
        "value": entities
    }
    
    return JSONResponse(content=response)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
