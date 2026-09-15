# High-Performance E-Commerce Backend Engine

A high-performance, asynchronous e-commerce backend API built with **FastAPI**, **PostgreSQL**, and **Redis**. Designed specifically to solve high-concurrency challenges in digital commerce platforms.

---

## Project Background & Objective

In high-traffic e-commerce platforms, flash sales and concurrent checkouts often lead to critical backend issues such as **overbooking** (selling items beyond available stock due to race conditions) and **database bottlenecks** from repetitive read queries.

This project was developed as a production-grade backend implementation to demonstrate:
1. **Concurrency Control:** Resolving race conditions at the microsecond level using distributed locking mechanisms.
2. **Read Optimization:** Minimizing database load using in-memory caching strategies.
3. **Modern Architecture:** Implementing asynchronous I/O and containerization ready for cloud deployment.

---

## Benefits & Core Functionality

- **Race Condition Prevention:** Guarantees that product inventory remains accurate and prevents double-selling under high concurrent user load.
- **Ultra-Low Latency Read Operations:** Delivers product catalog data directly from memory cache, significantly reducing API response times.
- **ACID-Compliant Transactions:** Ensures complete order and inventory state integrity using PostgreSQL's transactional guarantees.
- **Scalable Architecture:** Fully containerized setup enabling seamless horizontal scaling across cloud platforms.

---

## Key Technical Features

- **Atomic Stock Management:** Leverages **Redis Distributed Locks** (`redis.lock`) to ensure stock deduction operations are executed sequentially during concurrent requests.
- **High-Performance Caching:** Utilizes Redis as an in-memory cache for product catalog endpoints to bypass redundant PostgreSQL queries.
- **Async I/O Processing:** Built on **SQLAlchemy 2.0 Async ORM** paired with the `asyncpg` driver for non-blocking database queries.
- **Full Containerization:** Completely isolated environment using **Docker** and **Docker Compose** (FastAPI Web App, PostgreSQL 16, and Redis 7).
- **Interactive Documentation:** Native OpenAPI/Swagger UI integration for real-time API manual testing.

---

## Tech Stack

- **Backend Framework:** Python 3.11, FastAPI
- **Database:** PostgreSQL 16
- **In-Memory Cache & Lock Broker:** Redis 7
- **Database ORM:** Async SQLAlchemy 2.0
- **Containerization:** Docker & Docker Compose
- **Data Schema Validation:** Pydantic v2

---

## Project Structure

```text
ecommerce-backend/
├── app/
│   ├── api/          # Endpoints & Dependencies (v1)
│   ├── core/         # Database Engine & Configurations
│   ├── models/       # SQLAlchemy Database Models
│   ├── schemas/      # Pydantic Request & Response Models
│   ├── services/     # Core Business Logic (Order & Race Condition Handling)
│   └── main.py       # FastAPI Entrypoint
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
