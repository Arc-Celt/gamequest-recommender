import pandas as pd
import numpy as np
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import gradio as gr
import os
import ast
import codecs
from dotenv import load_dotenv

load_dotenv()

script_dir = os.path.dirname(os.path.abspath(__file__))
css_path = os.path.join(script_dir, 'style.css')
with codecs.open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

games_path = os.path.join(script_dir, '..', 'data', 'processed', 'games_with_ratings_cleaned.csv')
games = pd.read_csv(games_path)

list_columns = ['categories', 'genres', 'supported_languages', 'tags']

for col in list_columns:
    games[col] = games[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

games['first_screenshot'] = np.where(
    games['first_screenshot'].isna(),
    os.path.join(script_dir, "..", "images", "screenshot-not-found.png"),
    games['first_screenshot']
)

db_games = Chroma(
    persist_directory=os.path.join(script_dir, "..", "data", "chroma_storage"),
    embedding_function=OpenAIEmbeddings()
)

def retrive_semantic_recs(
    query: str,
    categories: list = None,
    genres: list = None,
    price_range: list = None,
    supported_languages: list = None,
    supported_systems: list = None,
    rating: list = None,
    initial_top_k: int = 100,
    final_top_k: int = 15,
    sort_by_rating: bool = False
) -> pd.DataFrame:
    recs = db_games.similarity_search(query, k=initial_top_k)
    game_ids = [int(recs[i].page_content.split()[0]) for i in range(len(recs))]
    game_recs = games[games['app_id'].isin(game_ids)]

    if categories and "Any" not in categories:
        game_recs = game_recs[game_recs['categories'].apply(
            lambda cats: any(cat in categories for cat in cats)
        )]

    if genres and "Any" not in genres:
        game_recs = game_recs[game_recs['genres'].apply(
            lambda gs: any(g in genres for g in gs)
        )]

    if price_range:
        if isinstance(price_range, list) and len(price_range) == 2:
            min_price, max_price = price_range
        else:
            min_price = 0
            max_price = price_range if isinstance(price_range, (int, float)) else 100

        game_recs = game_recs[
            (game_recs['price'] >= min_price) & (game_recs['price'] <= max_price)
        ]

    if supported_languages and "Any" not in supported_languages:
        game_recs = game_recs[game_recs['supported_languages'].apply(
            lambda langs: any(lang in supported_languages for lang in langs)
        )]

    if supported_systems and "Any" not in supported_systems:
        system_filters = [sys.lower() for sys in supported_systems if sys != "Any"]
        if system_filters:
            game_recs = game_recs[game_recs[system_filters].any(axis=1)]

    if rating and "Any" not in rating:
        game_recs = game_recs[game_recs['rating'].isin(rating)]

    if sort_by_rating:
        rating_order = [
            "Overwhelmingly Positive", "Very Positive", "Positive",
            "Mostly Positive", "Mixed", "Mostly Negative",
            "Negative", "Very Negative", "Overwhelmingly Negative", "No Reviews"
        ]
        rating_map = {r: i for i, r in enumerate(rating_order)}

        game_recs['rating_score'] = game_recs['rating'].map(
            lambda r: rating_map.get(r, len(rating_order))
        )
        game_recs = game_recs.sort_values(by='rating_score')

    return game_recs.head(final_top_k)


def recommend_games(
    query: str,
    categories: list = None,
    genres: list = None,
    price_range: list = None,
    supported_languages: list = None,
    supported_systems: list = None,
    rating: list = None,
    initial_top_k: int = 100,
    final_top_k: int = 15,
    sort_by_rating: bool = False
):
    if not query.strip():
        return []
    recommendations = retrive_semantic_recs(
        query=query,
        categories=categories,
        genres=genres,
        price_range=price_range,
        supported_languages=supported_languages,
        supported_systems=supported_systems,
        rating=rating,
        initial_top_k=initial_top_k,
        final_top_k=final_top_k,
        sort_by_rating=sort_by_rating
    )
    results = []

    for _, row in recommendations.iterrows():
        # Handle missing descriptions safely
        description = str(row.get('about_the_game', '')) if not pd.isna(row.get('about_the_game')) else ''
        truncated_description = (
            description[:50] + "..." if len(description) > 50
            else description
        )

        name = row['name']
        genres_str = ', '.join(row['genres']) if isinstance(row['genres'], list) else str(row['genres'])
        rating_str = str(row['rating']) if not pd.isna(row['rating']) else "No Rating"
        caption = f"{name} | {genres_str} | Rating: {rating_str} | {truncated_description}"
        results.append((row["first_screenshot"], caption))

    return results


status_message = gr.Markdown("", elem_id="status-message", visible=False)


def recommend_games_wrapper(
    query, categories, genres, min_price, max_price, 
    supported_languages, supported_systems, rating, 
    initial_top_k, final_top_k, sort_by_rating
):
    """Wrapper function that combines min and max price inputs"""
    try:
        price_range = [min_price, max_price]

        if not query.strip():
            return [], "✏️ Please enter a search query to find games."

        results = recommend_games(
            query=query,
            categories=categories,
            genres=genres,
            price_range=price_range,
            supported_languages=supported_languages,
            supported_systems=supported_systems,
            rating=rating,
            initial_top_k=initial_top_k,
            final_top_k=final_top_k,
            sort_by_rating=sort_by_rating
        )

        if not results:
            return [], "🔍 No games found. Try adjusting your filters."

        return results, f"🔍 Found {len(results)} games matching your criteria."

    except Exception as e:
        print(f"Error: {str(e)}")
        return [], "❌ An error occurred. Please try again."


categories_list = sorted(set([cat for cats in games['categories'] for cat in cats if isinstance(cats, list)]))
categories = ["Any"] + categories_list
genres_list = sorted(set([genre for genres in games['genres'] for genre in genres if isinstance(genres, list)]))
genres = ["Any"] + genres_list
price_range = [0, 60]
supported_languages_list = sorted(set([lang for langs in games['supported_languages'] for lang in langs if isinstance(langs, list)]))
supported_languages = ["Any"] + supported_languages_list
supported_systems = ["Any", "windows", "mac", "linux"]
ratings = ["Any", 'Overwhelmingly Positive', 'Very Positive',
           'Mostly Positive', 'Positive', 'Mixed', 'Negative',
           'Mostly Negative', 'Very Negative',
           'Overwhelmingly Negative', 'No Reviews']


with gr.Blocks(theme=gr.themes.Soft(), css=css) as dashboard:
    with gr.Column(elem_classes="main-container"):
        # Header section
        with gr.Row(elem_classes="header-row"):
            with gr.Column(elem_classes="header-content"):
                gr.Markdown("""
                # 🎮 GameQuest
                ## &nbsp; Your AI-powered game finder for your next gaming spree!
                """, elem_classes="header-title")

        # Filters section - using Row instead of Box
        with gr.Row(elem_classes="filters-container"):
            with gr.Column(elem_classes="filters-box"):
                # Put filters in horizontal rows instead of vertical columns
                with gr.Row(elem_classes="filters-row"):
                    # First filter group
                    with gr.Column(scale=1, elem_classes="filter-column"):
                        with gr.Accordion("Game Content", open=True, elem_classes="filter-group"):
                            category_dropdown = gr.Dropdown(
                                choices=categories,
                                label="Categories",
                                value="Any",
                                multiselect=True
                            )
                            genre_dropdown = gr.Dropdown(
                                choices=genres,
                                label="Genres",
                                value="Any",
                                multiselect=True
                            )

                    # Second filter group
                    with gr.Column(scale=1, elem_classes="filter-column"):
                        with gr.Accordion("Personal Settings", open=True, elem_classes="filter-group"):
                            system_dropdown = gr.Dropdown(
                                choices=supported_systems,
                                label="Platforms",
                                value="Any",
                                multiselect=True
                            )
                            language_dropdown = gr.Dropdown(
                                choices=supported_languages,
                                label="Languages",
                                value="Any",
                                multiselect=True
                            )

                    # Third filter group
                    with gr.Column(scale=1, elem_classes="filter-column"):
                        with gr.Accordion("Price & Rating", open=True, elem_classes="filter-group"):
                            # Price inputs on same row
                            with gr.Row(elem_classes="price-row"):
                                min_price_input = gr.Number(
                                    label="Min Price ($)",
                                    value=0,
                                    minimum=0,
                                    maximum=1000,
                                    step=1
                                )
                                max_price_input = gr.Number(
                                    label="Max Price ($)",
                                    value=60,
                                    minimum=0,
                                    maximum=1000,
                                    step=1
                                )
                            rating_dropdown = gr.Dropdown(
                                choices=ratings,
                                label="Rating",
                                value="Any",
                                multiselect=True
                            )

                # Search section - moved below filters
                with gr.Row(elem_classes="search-row"):
                    # Display options in the same row as search
                    with gr.Column(scale=1, elem_classes="display-options-column"):
                        with gr.Accordion("Display Options", open=True, elem_classes="filter-group"):
                            results_slider = gr.Slider(
                                minimum=5,
                                maximum=30,
                                value=10,
                                step=1,
                                label="Number of results"
                            )
                            sort_checkbox = gr.Checkbox(
                                label="Sort by user rating",
                                value=False
                            )

                    # Search input and button
                    with gr.Column(scale=3, elem_classes="search-column"):
                        user_query = gr.Textbox(
                            label="Describe the game you're looking for",
                            placeholder="e.g. A game with dragons and magic！",
                            value="",
                            elem_classes="search-input"
                        )
                        search_button = gr.Button("🔍 Find Games!", elem_classes="search-button")

        # Status message (feedback area)
        status_message = gr.Markdown("", elem_id="status-message", elem_classes="status-message")

        # Results section
        with gr.Row(elem_classes="results-row"):
            output = gr.Gallery(
                label="Game Recommendations",
                columns=4,
                height="auto",
                allow_preview=True,
                show_label=True,
                object_fit="contain",
                elem_id="gallery-output",
                elem_classes="gallery-custom"
            )

        # Footer
        with gr.Row(elem_classes="footer-row"):
            gr.Markdown("Built by Archer Liu 🐺", elem_classes="footer-text")

    search_button.click(
        fn=recommend_games_wrapper,
        inputs=[
            user_query,
            category_dropdown,
            genre_dropdown,
            min_price_input,
            max_price_input,
            language_dropdown,
            system_dropdown,
            rating_dropdown,
            gr.Number(value=100, visible=False),
            results_slider,
            sort_checkbox
        ],
        outputs=[output, status_message]
    )

if __name__ == "__main__":
    dashboard.launch(share=False)
