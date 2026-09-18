import requests
import chromadb

OLLAMA_URL = "http://localhost:11434"
EMBED_MODEL = "nomic-embed-text:latest"

# Connect to the local ChromaDB database
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="manuals")

# Sample Technical Manual Data
manual_data = [
    {
        "id": "manual_001",
        "text": "Centrifugal Pump Series 500 Safety Protocol: Maximum safe operating temperature is 80°C. If temperature exceeds 85°C, initiate emergency shutdown immediately, isolate power supply, and check bearing lubrication and mechanical seal."
    },
    {
        "id": "manual_002",
        "text": "Hydraulic Gate Valve GV-200 Specifications: Maximum allowable working pressure is 150 BAR. Always execute pressure relief procedures before loosening bonnet bolts for seal maintenance."
    },
    {
        "id": "manual_003",
        "text": "SCADA Industrial Boiler Operating Limits: Normal steam pressure range is 10 to 15 BAR. In case of a combustible gas leak alert, automatic safety system closes emergency fuel isolation valve EV-101 within 2 seconds."
    },
    {
        "id": "manual_004",
        "text": "Transformer Maintenance SOP: Transformer oil insulation breakdown voltage must remain above 30 kV. Oil oxidation and sludge formation occur when internal temperatures persistently exceed 90°C."
    },
    {
        "id": "manual_005",
        "text": "Pipeline Corrosion Prevention Guidelines: Internal pipeline corrosion is minimized by maintaining pH levels between 7.5 and 8.5 and injecting liquid corrosion inhibitors at intervals of 500 operating hours."
    }
]

print("Adding manuals to local vector database...")

for doc in manual_data:
    # Get embedding vector from local Ollama model
    res = requests.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": doc["text"]}
    ).json()
    
    embedding = res.get("embedding", [])
    
    # Store in ChromaDB
    collection.upsert(
        ids=[doc["id"]],
        documents=[doc["text"]],
        embeddings=[embedding]
    )
    print(f"Ingested: {doc['id']}")

print("\nSUCCESS: All technical manuals stored in ChromaDB!")