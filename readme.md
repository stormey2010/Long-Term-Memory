# Memory Management System

## Overview

This project includes a memory management system with functionalities for setting and retrieving memories, and a basic web UI for managing these memories. It uses Python scripts for memory extraction, retrieval, and database handling, and features a Flask-based web interface.

## Installation

### Prerequisites

- Python 3.x

### Install Required Packages

To install the required Python packages, use the following command:
```python
pip install flask sqlite3 groq
```

### Edit config.py

Go into memory/config.py to set api keys and configuration for personalization

### Project Structure

- `memory/`
    - `templates` - Folder for all html files
        - `add_item.html` 
        - `ai_add_item.html`
        - `index.html` 
        - `item_details.html` 
    - `config.py` - Makes easy editing for api keys, etc
  - `extract.py` - Handles extraction and setting of memories.
  - `retrive.py` - Handles retrieval of memories.
  - `db_handler.py` - Interfaces with `extract.py` and `retrive.py` for memory management.
  - `db.py` - Contains the Flask application and database functions.
- `example_script.py` - Demonstrates how to use the memory management system.

## Memory UI

The Flask-based web UI is available at:

http://127.0.0.1:5000

If there was an issue with this url run db.py file to find the url 
```python
python -m memory.db
```

## Usage

1. **Run the Example Script**

   To demonstrate how to use the memory management system, run the example script:

   python example_script.py

   This script will:
   - Set a memory.
   - Retrieve a memory.
   - Start the Memory UI.

2. **Interacting with the Memory UI**

   - **Home Page:** View all items in the database.
   - **Insert Item:** Add new items to the database.
   - **Search:** Search for items using keywords.
   - **Item Details:** View and update details of a specific item.
   - **Delete Item:** Remove individual items from the database.
   - **Delete All:** Remove all items from the database.
   - **AI Integration:** Add items using AI-generated memory settings.


