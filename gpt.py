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


def top_n(data: list, genre: str = '', n: int = 0):
    """
    Returns a sorted list of top movies based on the average rating of the movie's
    rating and the highest actor ratings across their films.
    
    Parameters:
    - data: List of movie data (each item is a list containing movie details).
    - genre: A string of movie genres (comma-separated) to filter by, or an empty string for all genres.
    - n: The number of top movies to return. If 0, all movies are returned.
    
    Returns:
    - A list of tuples, each containing (Title, Average_rating).

    >>> dat = [['1', 'Guardians of the Galaxy', 'Action,Adventure,Sci-Fi', 'A group of intergalactic \
criminals are forced to work together to stop a fanatical warrior from taking control of the universe.',\
 'James Gunn', 'Chris Pratt, Vin Diesel, Bradley Cooper, Zoe Saldana', '2014', '121', '8.1', '757074', \
'333.13', '76.0'], ['3', 'Split', 'Horror,Thriller', 'Three girls are kidnapped by a man with a diagnosed \
23 distinct personalities. They must try to escape before the apparent emergence of a frightful new 24th.', \
'M. Night Shyamalan', 'James McAvoy, Anya Taylor-Joy, Haley Lu Richardson, Jessica Sula', '2016', '117', \
'7.3', '157606', '138.12', '62.0']]
    >>> top_n(dat, genre='Action', n=1)
    [('Guardians of the Galaxy', 8.1)]
    
    >>> top_n(dat, genre='Horror,Thriller', n=0)
    [('Split', 7.3), ('Guardians of the Galaxy', 8.1)]

    >>> top_n(dat, genre='', n=1)
    [('Guardians of the Galaxy', 8.1)]
    """
    
    # Parse genres if provided
    genres = set(genre.split(',')) if genre else set()
    
    # Filter movies based on genres
    filtered_movies = []
    for movie in data:
        if not genres or any(g.strip() in movie[2] for g in genres):
            filtered_movies.append(movie)
    
    def highest_rating_for_actor(actor_name, all_movies):
        """
        Returns the highest rating for a given actor across all movies.
        
        Parameters:
        - actor_name: The name of the actor.
        - all_movies: List of all movie data.
        
        Returns:
        - The highest rating for the actor.
        """
        highest_rating = 0
        for movie in all_movies:
            if actor_name in movie[5]:
                rating = float(movie[8])
                if rating > highest_rating:
                    highest_rating = rating
        return highest_rating
    
    # List of tuples (Title, Rating, Actor_Rating)
    movie_tuples = []
    for movie in filtered_movies:
        title = movie[1]
        rating = float(movie[8])
        actors = movie[5].split(',')
        
        # Calculate actor rating as the average of the highest ratings of the actors
        total_actor_rating = 0
        for actor in actors:
            actor_rating = highest_rating_for_actor(actor.strip(), data)
            total_actor_rating += actor_rating
        
        actor_rating = total_actor_rating / len(actors) if actors else 0
        
        movie_tuples.append((title, rating, actor_rating))
    
    # Sort movies based on the average of Rating and Actor_Rating,
    # then lexicographically by title
    sorted_movies = []
    for movie_tuple in movie_tuples:
        inserted = False
        for i, sorted_movie in enumerate(sorted_movies):
            avg_rating = (sorted_movie[1] + sorted_movie[2]) / 2
            current_avg = (movie_tuple[1] + movie_tuple[2]) / 2
            if current_avg > avg_rating or (current_avg == avg_rating and movie_tuple[0] < sorted_movie[0]):
                sorted_movies.insert(i, movie_tuple)
                inserted = True
                break
        if not inserted:
            sorted_movies.append(movie_tuple)
    
    # Select top n or all movies if n == 0
    top_movies = sorted_movies[:n] if n > 0 else sorted_movies
    
    # Return in the format (Title, Average_rating)
    result = []
    for title, rating, actor_rating in top_movies:
        average_rating = (rating + actor_rating) / 2
        result.append((title, average_rating))
    
    return result


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
        for i, (title, avg_rating) in enumerate(top):
            # Write without a newline for the last element
            if i < len(top) - 1:
                file.write(f"{title}, {avg_rating:.1f}\n")
            else:
                file.write(f"{title}, {avg_rating:.1f}")
