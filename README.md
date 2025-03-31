# GameQuest

[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![Python 3.10.0](https://img.shields.io/badge/python-3.10.0-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Summary

GameQuest is an intelligent game recommender for Steam, the largest PC gaming platform, leveraging NLP techniques and vector search technology to match users with semantically relevant games. By transforming game descriptions into high-dimensional embeddings stored in a vector database (ChromaDB), GameQuest enables semantic similarity search to find games that are conceptually related to user queries, going beyond simple keyword matching. The system performs efficient nearest-neighbor search in the embedding space to identify games that are contextually similar to the user's interests. The dataset utilized in GameQuest is the [Steam Games Dataset](https://www.kaggle.com/datasets/fronkongames/steam-games-dataset), which includes information on over 97,000 games available on Steam.

## Live Demo

You can try out GameQuest without installing anything using the live demo:

🎮 **[Try GameQuest on HuggingFace Spaces](https://huggingface.co/spaces/celt313/gamequest)**

## Project Objectives

- [x] Clean and preprocess game data by handling missing values and extracting relevant features.
- [x] Convert game description into high-dimensional embeddings using OpenAI's embedding model.
- [x] Store embeddings in ChromaDB and use vector search for efficient game retrieval based on user queries.
- [x] Deliver personalized recommendations through an interactive interface.

## Technologies & Frameworks

- Python 3.10+
- OpenAI API (text-embedding-3-large)
- LangChain
- ChromaDB
- Gradio
- Pandas & NumPy
- Scikit-learn
- HuggingFace Spaces

## Setup and Installation

### ⚡Cloning the Repository Without Large Files

1. **Clone the repository**:

    This repository contains large dataset files tracked by Git LFS. If you only need the code and configurations without downloading large files, use the following command:

    ```bash
    git clone --filter=blob:none https://github.com/Arc-Celt/gamequest-recommender.git
    ```

    This will clone everything except large files tracked by Git LFS. If you later need the large files, you can download them selectively with:

    ```bash
    git lfs pull --include="PATH_TO_REQUIRED_FILES"
    ```

    Or download all LFS files:

    ```bash
    git lfs pull
    ```

2. **Set up and activate the virtual environment**:

    ```bash
    conda env create -f environment.yml
    conda activate gamequest
    ```

3. **Run the application**:

    ```bash
    python src/dashboard.py
    ```

    This will start a local server, and you can access the application in your web browser at `http://localhost:7860`.

## Support

Encountering issues? Need assistance? For any questions regarding this dashboard, please open an issue in the GitHub repository.

## Contributing

Interested in contributing? Check out the contributing guidelines at [CONTRIBUTING.md](https://github.com/Arc-Celt/gamequest-recommender/blob/main/CONTRIBUTING.md) for details. Please note that this project is released with a [Code of Conduct](https://github.com/Arc-Celt/gamequest-recommender/blob/main/CODE_OF_CONDUCT.md). By contributing to this project, you agree to abide by its terms.

## License

`GameQuest` was created by Archer Liu. It is licensed under the terms of the [MIT](https://github.com/Arc-Celt/gamequest-recommender/blob/main/LICENSE) license.
