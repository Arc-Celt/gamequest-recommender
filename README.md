# GameQuest

**Author:** Archer(Rongze) Liu

## Summary

GameQuest is an intelligent game recommender for Steam, the largest PC gaming platform, leveraging Natural Language Processing (NLP) techniques and word embeddings to match users with semantically relevant games based on their input queries. By transforming game descriptions into high-dimensional embeddings, GameQuest enables users to explore games that are contextually similar to their interests. The dataset utilized in GameQuest is the [Steam Games Dataset](https://www.kaggle.com/datasets/fronkongames/steam-games-dataset), which includes information on over 97,000 games available on Steam.

## Project Objectives

- [x] Clean and preprocess game data by handling missing values and extracting relevant features.
- [x] Convert game description into high-dimensional embeddings using OpenAI's embedding model.
- [x] Store embeddings in ChromaDB and use vector search for efficient game retrieval based on user queries.
- [x] Deliver personalized recommendations through an interactive interface.

## ⚡Cloning the Repository Without Large Files

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
