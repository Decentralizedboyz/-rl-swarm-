# Black Bull Investments Dashboard

A modern, futuristic investment dashboard with advanced features for crypto and traditional investments.

## Features

- **User Authentication**: Secure login and registration system
- **Investment Tracking**: Monitor your investments in real-time
- **Payment Processing**: Support for multiple payment methods
- **VIP Meme Coins**: Exclusive access to premium meme coins
- **P2P Smart Flex**: Peer-to-peer transactions with multiple currencies
- **Strategic Partners**: Integration with major crypto platforms
- **Smart Leverage AI**: Advanced trading predictions and strategies

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, JWT Authentication
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Database**: SQLite
- **Styling**: Custom futuristic design with nano-tech elements

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/rl-swarm.git
cd rl-swarm/client_dashboard
```

2. Install dependencies:
```bash
pip3 install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Initialize the database:
```bash
python3 backend/database/init_db.py
```

## Running the Application

1. Start the backend server:
```bash
python3 -m uvicorn backend.server:app --reload --host 0.0.0.0 --port 8000
```

2. Start the frontend server:
```bash
python3 serve.py
```

3. Access the application:
- Frontend: http://localhost:8080
- API Documentation: http://localhost:8000/docs

## Project Structure

```
client_dashboard/
├── backend/
│   ├── database/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── init_db.py
│   │   └── models.py
│   ├── __init__.py
│   └── server.py
├── frontend/
│   ├── assets/
│   │   └── partners/
│   ├── index.html
│   ├── login.html
│   └── register.html
├── .env
├── requirements.txt
├── run.py
├── serve.py
└── setup.py
```

## API Endpoints

- `/token` - Authentication
- `/users/register` - User registration
- `/users/me` - Get user info
- `/investments` - Investment management
- `/payments` - Payment processing
- `/notifications` - User notifications

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 