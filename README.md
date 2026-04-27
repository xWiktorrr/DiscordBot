# 🏁 VelocityObecnosc – Discord F1 Signup Bot

Bot Discord napisany w Pythonie do zarządzania zapisami na wyścigi (np. ligi F1).

## 🚀 Funkcje

* ✅ Zapisy do zespołów przez przyciski (buttons)
* ✅ Automatyczne przypisywanie do teamów
* ✅ Limity miejsc w zespołach (np. 2/2)
* ✅ Rezerwa i "Nie jadę"
* ✅ Embed z aktualną listą kierowców
* ✅ Custom emoji dla zespołów
* ✅ Ograniczenie dostępu do komend (role)
* ✅ Automatyczne zamknięcie zapisów (timer)
* ✅ Sprawdzanie czy użytkownik ma odpowiednią rolę

---

## 📸 Preview

Bot wyświetla embed z zespołami i przyciskami do zapisów:

* Alpine, Ferrari, Mercedes itd.
* Kliknięcie przycisku = zapis do zespołu
* Automatyczna aktualizacja listy

---

## ⚙️ Instalacja

### 1. Klonuj repo

```bash
git clone https://github.com/TWOJ_LOGIN/VelocityObecnosc.git
cd VelocityObecnosc
```

### 2. Stwórz virtual environment

```bash
python -m venv venv
```

### 3. Aktywuj venv

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/Mac:**

```bash
source venv/bin/activate
```

### 4. Zainstaluj zależności

```bash
pip install discord.py
```

---

## 🔑 Konfiguracja

W pliku `.py` ustaw:

```python
TOKEN = "TWÓJ_DISCORD_TOKEN"
```

Opcjonalnie:

* ID ról (dla ograniczeń)
* ID emoji (dla zespołów)
* DATA zamknięcia zapisów

---

## ▶️ Uruchomienie

```bash
python VelocityObecnosc.py
```

---

## 🧠 Jak działa

* Bot wysyła embed z zespołami
* Użytkownik klika przycisk
* Bot zapisuje go do teamu (JSON)
* Embed aktualizuje się automatycznie

---

## 📁 Struktura

```
VelocityObecnosc/
│
├── VelocityObecnosc.py
├── data.json
└── README.md
```

---

## 🔒 Wymagania

* Python 3.10+
* discord.py

---

## 💡 Plany / TODO

* [ ] Panel admina
* [ ] Historia zapisów
* [ ] Automatyczne resetowanie rund
* [ ] Integracja z kalendarzem

---

## 🧑‍💻 Autor

Projekt stworzony na potrzeby serwera Discord F1 w 100% mojego autorstwa.

---

## ⚠️ Uwaga

Bot wymaga włączonych intents w Discord Developer Portal:

* MESSAGE CONTENT INTENT
* SERVER MEMBERS INTENT

---

## ⭐ Jeśli działa – zostaw star

😎
