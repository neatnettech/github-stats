
# Git Stats Aggregator

This project is a Python script that collects and aggregates Git statistics from local repositories and generates a visually appealing card summarizing global stats as an image.

## Features

- Recursively scans a directory for all Git repositories.
- Collects commit statistics for a specific year (default: 2024).
- Aggregates global stats, including:
  - Total number of commits.
  - Most active month.
  - Most active day of the week.
  - Top programming language based on file extensions.
- Generates a single card-style image summarizing the global stats.

## Example Output

A single card is generated as an image with the following details:
- **Total Commits:** The aggregate number of commits across all repositories.
- **Most Active Month:** The month with the highest commits.
- **Most Active Day:** The most active day of the week for commits.
- **Top Language:** The most commonly used file extension.

## Requirements

- Python 3.7+
- Pillow (Python Imaging Library)

## Installation

1. Clone this repository or download the script.
2. Install dependencies:
   ```bash
   pip install pillow
   ```

## Usage

1. Place all your repositories in a single directory (e.g., `/path/to/your/repos`).
2. Update the `ROOT_DIR` constant in the script to the path of your repositories directory:
   ```python
   ROOT_DIR = "/path/to/your/repos"
   ```
3. Update the font path (`FONT_PATH`) in the script to a font available on your system (e.g., DejaVu Sans on Linux):
   ```python
   FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
   ```
4. Run the script:
   ```bash
   python script_name.py
   ```

## Output

- The global statistics will be displayed in the terminal.
- A card image summarizing the global stats will be saved as `global_stats.png` in the current directory.

## Example Global Stats (Terminal Output)

```plaintext
Global Stats:
Total Commits: 1234
Most Active Month: July
Most Active Day: Tuesday
Top Language: .py
```

## Customization

- **Year:** Change the year for which stats are collected by modifying the `YEAR` constant:
  ```python
  YEAR = 2024
  ```
- **Card Design:** Modify dimensions, colors, and fonts by editing the `CARD_WIDTH`, `CARD_HEIGHT`, `BACKGROUND_COLOR`, and related constants.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
