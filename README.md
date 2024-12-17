
# Cafe API Flask Application

This is a simple Flask-based API that provides information about cafes, allows the addition, updating, and deletion of cafe records in a database, and includes functionality to get random cafes and search by location.

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Home Page](#home-page)
  - [Endpoints](#endpoints)
    - [GET /random](#get-random)
    - [GET /all](#get-all)
    - [GET /search/<location>](#get-search)
    - [POST /add](#post-add)
    - [PATCH /update_price/<id>](#patch-update-price)
    - [DELETE /report-closed/<id>](#delete-report-closed)
- [Contributing](#contributing)

## Requirements

- Python 3.x
- Flask
- Flask-SQLAlchemy
- SQLAlchemy

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MostafaHima/Cafe-API-Flask-Application.git
   cd Cafe-API-Flask-Application
   ```

2. Install the required packages using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database by running the Flask application:
   ```bash
   flask run
   python main.py
   ```

## Usage

### Home Page

The home page of the application is a simple interface that can be accessed by visiting `http://localhost:5000` after running the Flask application. It renders an `index.html` template.

### Endpoints

#### GET /random

This endpoint returns a random cafe from the database.

**Response:**
- `200 OK` with a JSON object containing the cafe details.

#### GET /all

This endpoint retrieves all cafes from the database and returns them as a JSON array.

**Response:**
- `200 OK` with a JSON object containing all cafe records.

#### GET /search/<location>

This endpoint searches for cafes in a specific location.

**Example Request:**
- `/search/London`

**Response:**
- `200 OK` with a JSON object containing the cafe details if found.
- `404 Not Found` if no cafes are found in that location.

#### POST /add

This endpoint allows adding a new cafe record to the database.

**Request Body (form-data):**
- `name`: Name of the cafe
- `map_url`: URL for the map location of the cafe
- `img_url`: Image URL of the cafe
- `location`: Location of the cafe
- `has_sockets`: Boolean (True/False) indicating if the cafe has power sockets
- `has_toilet`: Boolean (True/False) indicating if the cafe has toilets
- `has_wifi`: Boolean (True/False) indicating if the cafe has Wi-Fi
- `can_take_calls`: Boolean (True/False) indicating if the cafe allows taking calls
- `seats`: Seating capacity of the cafe
- `coffee_price`: Price of a coffee at the cafe

**Response:**
- `200 OK` with a success message.

#### PATCH /update_price/<id>

This endpoint allows updating the coffee price for a specific cafe by its `id`.

**Request Parameters:**
- `new_price`: The new price for the coffee.

**Response:**
- `200 OK` with a success message.
- `404 Not Found` if the cafe is not found by the provided `id`.

#### DELETE /report-closed/<id>

This endpoint allows deleting a cafe record by its `id`. Requires an API key.

**Request Parameters:**
- `api-key`: An API key for authentication.

**Response:**
- `200 OK` with a success message if the cafe is deleted.
- `403 Forbidden` if the API key is incorrect.
- `404 Not Found` if the cafe with the provided `id` does not exist.
