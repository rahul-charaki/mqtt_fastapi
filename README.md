# MQTT FastAPI Application

This repository contains a FastAPI-based application integrated with RabbitMQ for messaging and MongoDB for storing and querying data. The project demonstrates a simple implementation of a publish/subscribe pattern using RabbitMQ and provides APIs to interact with the system.

---

## Features

- **MQTT Emitter**: Simulates the publishing of messages to RabbitMQ with randomized status and timestamp data.
- **MQTT Processor**: Consumes messages from RabbitMQ and stores them in MongoDB.
- **FastAPI API**: Exposes an endpoint to query the database for message counts within a specific time range.

---

## Installation

### Prerequisites

1. **Python 3.8+**
2. **MongoDB**: Ensure MongoDB is installed and running locally.
3. **RabbitMQ**: Ensure RabbitMQ is installed and running locally.

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/username/mqtt-fastapi-app.git
   cd mqtt-fastapi-app
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start RabbitMQ and MongoDB services:
   - RabbitMQ: `sudo systemctl start rabbitmq-server`
   - MongoDB: `sudo systemctl start mongod`

5. Run the application:
   ```bash
   python main.py
   ```

---

## Project Structure

```
.
├── app
│   ├── __init__.py
│   ├── emitter.py          # MQTT Emitter logic
│   ├── processor.py        # MQTT Processor logic
│   ├── database.py         # MongoDB connection and helper functions
│   ├── api.py              # FastAPI routes and endpoints
├── main.py                 # Entry point of the application
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

---

## Usage

### APIs

- **POST /status_counts**

  Query message counts by status within a specific time range.

  **Request Body:**
  ```json
  {
      "start_time": "2023-11-01T00:00:00",
      "end_time": "2023-11-30T23:59:59"
  }
  ```

  **Response Example:**
  ```json
  {
      "0": 10,
      "1": 15,
      "2": 5,
      "3": 20
  }
  ```

### Background Services

- The emitter and processor services run as threads to simulate real-time message production and consumption.

---

## Contributing

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-name
   ```
5. Create a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## Acknowledgments

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pika (RabbitMQ Client)](https://pika.readthedocs.io/)
- [MongoDB Documentation](https://www.mongodb.com/docs/)

---


