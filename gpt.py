def read_file(pathname: str, year: int = 0):
    """
    Reads movie data from a semicolon-delimited file and returns a list of movies.

    Each movie is represented as a list of values from the file.
    Optionally, only movies from the specified `year` onward are included.

    Parameters:
        pathname (str): The path to the file containing the movie data.
        year (int): The starting year for filtering movies (default is 0, meaning no filter).

    Returns:
        list: A list of lists, where each inner list contains details of one movie.
    """
    movies = []
    with open(pathname, mode='r', encoding='utf-8') as file:
        next(file)  # Skip the header row

        for line in file:
            row = line.strip().split(';')
            movie_year = int(row[6])  # Year is the 7th field in the file (index 6)
            if movie_year >= year:
                movies.append(row)

    return movies


def get_highest_ratings(data: list) -> dict:
    """
    Calculate the highest rating for each actor across all movies.
    
    Args:
        data: A list of movie information, where each movie is represented
              as a list containing [title, rating, genres, actors].

    Returns:
        A dictionary where keys are actor names and values are the highest
        rating of any movie that actor appears in.

    >>> get_highest_ratings([
    ...     ['Movie A', '8.5', 'Action', 'Actor 1, Actor 2'],
    ...     ['Movie B', '7.0', 'Drama', 'Actor 1, Actor 3'],
    ...     ['Movie C', '9.0', 'Action', 'Actor 2, Actor 4']
    ... ])
    {'Actor 1': 8.5, 'Actor 2': 9.0, 'Actor 3': 7.0, 'Actor 4': 9.0}
    """
    actor_highest_ratings = {}
    for movie in data:
        title, rating, genres, actors = movie[0], float(movie[1]), movie[2], movie[3]
        for actor in actors.split(','):
            actor = actor.strip()
            if actor in actor_highest_ratings:
                actor_highest_ratings[actor] = max(actor_highest_ratings[actor], rating)
            else:
                actor_highest_ratings[actor] = rating
    return actor_highest_ratings

def average(numbers: list) -> float:
    """
    Calculate the average of a list of numbers.
    
    Args:
        numbers: A list of numbers.

    Returns:
        The average of the numbers. Returns 0 if the list is empty.

    >>> average([10, 20, 30])
    20.0
    >>> average([])
    0
    """
    if not numbers:
        return 0
    total = sum(numbers)
    count = len(numbers)
    return total / count

def top_n(data: list, genre: str = '', n: int = 0) -> list:
    """
    For each movie in data with the specified genre(s), calculates a new rating
    `actor_rating` as the mean of the highest ratings for each actor appearing
    in the movie.

    Args:
        data: A list of movie information.
        genre: A movie genre or comma-separated list of genres.
        n: The number of movies to return. If n=0, returns all matching movies.

    Returns:
        A list of tuples in the format (Title, Average_rating), sorted in
        descending order based on the average of Rating and Actors_Rating.
    
    >>> top_n([['Dangal', '8.8', 'Action', 'Aamir Khan'], 
    ...        ['Bahubali: The Beginning', '8.3', 'Action', 'Prabhas'],
    ...        ['Guardians of the Galaxy', '8.1', 'Action', 'Chris Pratt'],
    ...        ['Mad Max: Fury Road', '8.1', 'Action', 'Tom Hardy'],
    ...        ['Star Wars: Episode VII - The Force Awakens', '8.1', 'Action', 'Daisy Ridley']],
    ...       genre='Action', n=5)
    [('Dangal', 8.8), ('Bahubali: The Beginning', 8.3), ('Guardians of the Galaxy', 8.1), \
('Mad Max: Fury Road', 8.1), ('Star Wars: Episode VII - The Force Awakens', 8.1)]
    """
    actor_highest_ratings = get_highest_ratings(data)
    genre_set = set(g.strip().lower() for g in genre.split(',')) if genre else None
    
    movies_with_actor_ratings = []
    for movie in data:
        title, rating, genres, actors = movie[0], float(movie[1]), movie[2], movie[3]
        genres_list = set(g.strip().lower() for g in genres.split(','))
        
        if genre_set is None or genre_set & genres_list:
            actor_ratings = [
                actor_highest_ratings[actor.strip()]
                for actor in actors.split(',')
                if actor.strip() in actor_highest_ratings
            ]
            actor_rating = average(actor_ratings) if actor_ratings else rating
            movies_with_actor_ratings.append((title, rating, actor_rating))
    
    # Sort movies based on average of rating and actor_rating, then by title
    sorted_movies = sorted(
        movies_with_actor_ratings,
        key=lambda movie: (-(movie[1] + movie[2]) / 2, movie[0])
    )
    
    # Prepare the result list with average ratings
    top_movies = []
    for title, rating, actor_rating in sorted_movies:
        avg_rating = (rating + actor_rating) / 2
        top_movies.append((title, avg_rating))
    
    return top_movies[:n] if n > 0 else top_movies

def write_file(top: list, file_name: str):
    """
    Writes each tuple (Title, rating) from the list `top` to the file `file_name`.

    Args:
        top: A list of tuples with (Title, rating).
        file_name: The name of the file to write the output to.

    Example:
    If `top` is [('Intern', 8.5)], then the file content should be:
    
    Intern, 8.5

    >>> write_file([('Dangal', 8.8), ('Bahubali', 8.3)], 'test_output.txt')
    >>> with open('test_output.txt', 'r') as f:
    ...     print(f.read().strip())
    Dangal, 8.8
    Bahubali, 8.3
    """
    with open(file_name, 'w') as file:
        for title, avg_rating in top:
            file.write(f"{title}, {avg_rating:.1f}\n")
