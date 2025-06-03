# 📝 Todoist Clean Architecture

A modern, clean-architecture inspired Todo app built with Python, SQLAlchemy, and PostgreSQL.

---

## 🚀 Features

- ✅ Create, update, and delete todos
- 📅 Set due dates and priorities
- 🔔 Mark tasks as completed
- 🏷️ User-based task management
- 🏗️ Clean, maintainable codebase using best practices

---

## 🏛️ Architecture

This project follows the **Clean Architecture** principles:

- **Entities**: Business models and logic
- **Use Cases**: Application-specific business rules
- **Interfaces**: Database, API, and external services
- **Frameworks & Drivers**: SQLAlchemy, FastAPI, etc.

```
src/
├── entities/
├── use_cases/
├── interfaces/
├── database/
└── ...
```

---

## ⚡ Quickstart

1. **Clone the repo**
   ```bash
   git clone https://github.com/Just2Deep/todo-clean.git
   cd todo-clean/todoist
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   - Copy `.env.example` to `.env` and set your variables.

4. **Run migrations**
   ```bash
   alembic upgrade head
   ```

5. **Start the app**
   ```bash
   uvicorn main:app --reload
   ```

---

## 🛠️ Tech Stack

- **Python 3.13+**
- **SQLAlchemy 2.0**
- **PostgreSQL**
- **FastAPI** 
- **Alembic** (migrations)

---

## 🤝 Contributing

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📄 License

MIT License

---

> Made with ❤️ by Deep!
