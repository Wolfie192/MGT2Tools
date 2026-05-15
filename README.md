# MGT2 Display Tool

Welcome, Referee! The **MGT2 Display Tool** is a sci-fi themed dual-window application designed for tabletop RPGs (like Traveller). It allows a Referee to push formatted information, tables, and lore snippets from a **Control Panel** to a dedicated **Player Display**—perfect for a second monitor or a shared screen.

![Sci-Fi Interface](https://img.shields.io/badge/Interface-Futuristic-00f2ff)
![Python](https://img.shields.io/badge/Python-3.9+-blue)

## Quick Start

### 1. Install Python
If you don't have Python yet, download it from [python.org](https://www.python.org/downloads/). 
* **Note:** During installation on Windows, make sure to check the box that says **"Add Python to PATH"**.

### 2. Download this Project
Click the green **"Code"** button at the top of this GitHub page and select **"Download ZIP"**. Extract that folder somewhere on your computer (like your Desktop).

### 3. Install the "Engines"
Open your computer's terminal (search for `cmd` or `PowerShell` on Windows) and type the following, then press Enter:
```bash
pip install PyQt6 markdown
```

### 4. Run the App
Double-click the `main.py` file, or run it from your terminal:
```bash
python main.py
```

---

## 🎮 How to Use

Once launched, you will see two windows:
1.  **Control Panel:** Keep this on your screen. It contains buttons for every "screen" defined in your data.
2.  **Player Display:** Drag this to your players' monitor and maximize it.

Clicking a button on the Control Panel instantly updates the Player Display with a high-contrast, futuristic layout.

---

## 🛠 Customizing Your Content

The coolest part of this tool is that you can write your own adventure data without touching the code. All the text lives in a file called `screens.xml`.

You can open `screens.xml` in any text editor (like Notepad) to add your own buttons. Here is a quick breakdown of how it works:

```xml
<screen button_group="Arrival" title="Starport" button_text="Arrival Info">
    <paragraph heading="Security">Please have your ID ready.</paragraph>
    <ul>
        <li bold="Law Level">High (8)</li>
        <li>No weapons allowed outside the terminal.</li>
    </ul>
    <table>
        <columns>Service | Cost</columns>
        <row>Refined Fuel | 500cr</row>
        <row>Unrefined Fuel | 100cr</row>
    </table>
</screen>
```

*   **button_group**: Groups buttons together in the control panel.
*   **title**: The big amber heading shown to players.
*   **button_text**: What the button says on your referee panel.
*   **Markdown Support**: You can use bold (`**text**`), italics (`*text*`), and lists inside paragraphs!

---

## 🛠 Requirements

If you prefer to use a virtual environment, the dependencies are:
*   **PyQt6**: Powers the windows and buttons.
*   **Markdown**: Handles the text formatting.

---