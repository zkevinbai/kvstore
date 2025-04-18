# Key-Value Store API

A simple key-value store built with FastAPI, designed to store and retrieve key-value pairs through HTTP endpoints.

## Requirements

- Python 3.7+
- `pip` for managing dependencies (or conda if preferred)

## Setup

1. Clone this repository:

   git clone https://github.com/your-username/kvstore.git
   cd kvstore

2. Create a virtual environment and activate it:

   - **macOS/Linux:**
     python -m venv venv
     source venv/bin/activate

   - **Windows:**
     python -m venv venv
     venv\Scripts\activate

3. Install dependencies:

   pip install -r requirements.txt

4. Run the server:

   python server.py

The service will run on `http://localhost:4000`.

## API Endpoints

- **GET /get/{key}**  
  Retrieves the value of a given key.

- **POST /set**  
  Sets a key-value pair.  
  **Body:**  
  {
    "key": "your_key",
    "value": "your_value"
  }

- **DELETE /delete/{key}**  
  Deletes the specified key.

## Testing

You can test the API using Postman, curl, or simply your browser.

**Example with curl:**

- Set a key-value pair:
  curl -X POST http://localhost:4000/set -H "Content-Type: application/json" -d '{"key":"foo","value":"bar"}'

- Get the value of a key:
  curl http://localhost:4000/get/foo

- Delete a key:
  curl -X DELETE http://localhost:4000/delete/foo

---

**License**: MIT

## features

### persist store to local json file

### add rate limiting, no more than 5 requests in a minute of any kind
* read the ip coming in
* track the ips in memory, list of timestamps of calls
* clean up mechanism, older than a minute, not relevant
* block over limit clients

### add authentication (hardcoded)