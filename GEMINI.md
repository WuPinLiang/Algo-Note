# Project Overview

This repository serves as the source for a personal blog, built using MkDocs. It is used to publish and manage various notes, articles, and thoughts, potentially including technical content like algorithms and data structures.

## Key Files

*   **`mkdocs.yml`**: The main configuration file for the MkDocs site. It defines the blog's structure, navigation, theme, and any plugins used.
*   **`requirements.txt`**: Lists the Python dependencies required to build and run the MkDocs site (e.g., `mkdocs`, `mkdocs-material`).
*   **`split_apcs.py`**: A Python script, likely used for specific content processing or organization, possibly related to the APCS notes within the blog.
*   **`docs/`**: This directory contains the primary Markdown files that form the content of the blog. It's where new posts and pages are typically added.
*   **`apcs/`**: This subdirectory contains specific notes related to APCS (Advanced Placement Computer Science), which are integrated into the blog's content.

## Building and Running

To build and serve the blog locally, follow these steps:

1.  **Install dependencies**: Ensure you have Python and `pip` installed. Then, install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Serve the site**: Navigate to the root of this repository in your terminal and run:
    ```bash
    mkdocs serve
    ```
    This will start a local development server, usually accessible at `http://127.0.0.1:8000`.

## Usage

This repository is used to author content in Markdown, which is then processed and rendered into a static website by MkDocs. Changes to Markdown files in the `docs/` or `apcs/` directories will be reflected when the site is built or served. The generated static site can then be deployed to a web server or hosting service.