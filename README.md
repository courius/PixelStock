
# PixelStock — Inventory Manager

A retro-styled, GUI-based inventory management system built in Python, designed for small shops and sole traders who need to track stock without the complexity of enterprise-grade software.

> 🏆 Built for the **Built with Python Hackathon** by **CS4Everyone**, hosted on Devpost.

---

<img width="2880" height="1806" alt="Image" src="https://github.com/user-attachments/assets/8f9532f2-29d0-478c-b63c-4ba0803e6368" />

## About the project

PixelStock started life as a basic terminal-based inventory script from my first year of college. For this hackathon, I went back to that original idea and rebuilt it from the ground up into a full graphical application — same core logic, completely new experience. Instead of typing numbers into a terminal prompt, you now get a proper interface: a login screen, a central "screen" display styled like an old terminal, sliding forms for input, live stock and value totals, and a save confirmation when you exit.

The goal was to build something that actually feels like a tool a small shop owner could open and use day to day, not just a script that technically works.

## Features

- **Login screen** to gate access to the system
- **View all products** in a formatted, scrollable table
- **Add new products** with full input validation
- **Update stock** for sales and deliveries, with live lookup of current stock
- **Edit product details** (name, category, price, minimum stock level)
- **Remove products** with confirmation and safeguards
- **Search** by product name (partial match) or exact category
- **Low stock alerts** with suggested reorder quantities
- **Category reports** — view stats for all categories or a single one
- **Transaction log** with an adjustable number of recent entries shown
- **Export reports** to CSV (full inventory, low stock) or a formatted `.txt` report
- **Live top-bar stats** — total inventory value and product count, updated in real time
- **Persistent storage** — inventory and transaction history are saved to JSON files between sessions
- **Save & Exit** flow with a "Saving... / Saved" confirmation screen

## Built with

- **Python** — core language
- **CustomTkinter** — modern GUI framework used for the entire interface (buttons, frames, entries, textboxes, sliders, progress bars)
- **Tkinter** — the underlying standard library toolkit CustomTkinter is built on
- **Pillow (PIL)** — image handling for backgrounds, the login avatar, and button graphics
- **JSON** — used for persistent storage of inventory and transaction data
- **CSV** — used for exporting inventory and low-stock reports

No external databases, APIs, or cloud services are used — everything runs locally and stores data in plain JSON files alongside the program.

## Project structure

```
.
├── main.py                     # Entry point — builds and runs the GUI
├── data_handler.py             # Loading, saving, and exporting data (JSON/CSV/TXT)
├── inventory.py                # Inventory class — manages the collection of products
├── product.py                  # Product class — represents a single inventory item
├── transaction_operations.py   # Logging of stock-changing transactions
├── inventory.json              # Saved inventory data (created/updated automatically)
├── transactions.json           # Saved transaction history (created/updated automatically)
└── ASSETS/                     # Background, avatar, and button images (optional)
```

## Getting started

### Requirements

- Python 3.9 or later
- The following packages:

```bash
pip install customtkinter pillow
```

### Running the app

Clone the repository, install the requirements above, then simply run:

```bash
python main.py
```

That's it — the application window will open, starting with the login screen.

### Logging in

The login screen uses a fixed demo set of credentials:

- **Username:** `iamtheuser`
- **Password:** `1234`

### Saving your data

Inventory and transaction data are saved automatically when you use the **Save & Exit** button in the app. Closing the window any other way will not save your changes, so make sure to exit through the button.

## Notes on assets

The app looks for optional image files inside an `ASSETS/` folder (a background image, a login avatar, and button graphics). If these files aren't present, the app falls back gracefully to plain colours and emoji icons — so it will run correctly even without any custom images supplied.

## Acknowledgements

This project builds on a basic terminal-based inventory script I originally wrote in my first year of college, reworked here into a full GUI application for the **Built with Python Hackathon** by CS4Everyone.
