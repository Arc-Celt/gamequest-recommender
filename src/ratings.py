import pandas as pd


def calculate_rating(positive, negative):
    """
    Calculate the Steam rating based on the number of positive and negative reviews.
    """
    if pd.isnull(positive) or pd.isnull(negative):
        return "No Reviews"

    try:
        positive = int(positive)
        negative = int(negative)

    except (ValueError, TypeError):
        return "No Reviews"
    total = positive + negative
    if total == 0:
        return "No Reviews"
    ratio = (positive / total) * 100

    if ratio >= 95 and total >= 500:
        return "Overwhelmingly Positive"
    elif ratio >= 85 and total >= 50:
        return "Very Positive"
    elif ratio >= 80:
        return "Positive"
    elif ratio >= 70:
        return "Mostly Positive"
    elif ratio >= 40:
        return "Mixed"
    elif ratio >= 20:
        return "Mostly Negative"
    elif ratio > 0 and total >= 500:
        return "Overwhelmingly Negative"
    elif ratio > 0 and total >= 50:
        return "Very Negative"
    else:
        return "Negative"


def main():
    """
    Load the game data, calculate ratings, and save the updated DataFrame to a CSV file.
    """
    input_path = 'data/processed/games_with_emotions.csv'
    output_path = 'data/processed/games_with_ratings.csv'

    df = pd.read_csv(input_path)
    df['rating'] = df.apply(lambda row: calculate_rating(row['positive'], row['negative']), axis=1)
    df.to_csv(output_path, index=False, encoding='utf-8')


if __name__ == "__main__":
    main()
