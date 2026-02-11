DROP TABLE IF EXISTS expenses;

CREATE TABLE expenses (
  id INTEGER PRIMARY KEY,
  amount REAL NOT NULL,
  date TEXT NOT NULL,
  category TEXT NOT NULL,
  note TEXT
);
