"""
a code-based service that allows the user to specify the genre,
the year, and the number of top rated movies they want to receive and 
returns to them a list of matching movies ordered by rating in descending order.
"""

def read_file(pathname: str, year: int=0) -> list[list]:
    """
    function reads data from file 
    and sorts it by year (given by user)

    :param pathname: str, path to file with movies
    :param year: int, year given by user
    :return: list[list], filtered data by year

    >>> read_file('films.csv', 2014)[:2]
    [['1', 'Guardians of the Galaxy', 'Action,Adventure,Sci-Fi', 'A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe.', 'James Gunn', 'Chris Pratt, Vin Diesel, Bradley Cooper, Zoe Saldana', '2014', '121', '8.1', '757074', '333.13', '76.0'], ['3', 'Split', 'Horror,Thriller', 'Three girls are kidnapped by a man with a diagnosed 23 distinct personalities. They must try to escape before the apparent emergence of a frightful new 24th.', 'M. Night Shyamalan', 'James McAvoy, Anya Taylor-Joy, Haley Lu Richardson, Jessica Sula', '2016', '117', '7.3', '157606', '138.12', '62.0']]
    """
    res_data = []
    with open(pathname, 'r', encoding="utf-8") as file:
        for line in file:
            if line[0].isdigit():
                line = line.strip().split(';')
                year_of_production = line[6]
                if year <= int(year_of_production):
                    res_data.append(line)
    return res_data

def top_n(data: list[list], genres: str='', n: int=0) -> list[tuple]:
    """
    function filters movies by genre, actors rating 
    (arithmetic mean of the top movie ranking for each actor), 
    movie rating and amount of movies

    :param data: list, list with movies filtered in read_file function
    :param genres: str, genre of a movie
    :param n: int, amount of movies to be shown for user
    :return: list[tuple], filtered list of movies

    >>> top_n(read_file('films.csv', 2014), genres='Action', n=5)
    [('Dangal', 8.8), \
('Bahubali: The Beginning', 8.3), \
('Guardians of the Galaxy', 8.1), \
('Mad Max: Fury Road', 8.1), \
('Star Wars: Episode VII - The Force Awakens', 8.1)]
    """
    def calculate_actors_rating(movie: list[str], data: list[list]) -> float:
        """
        Calculates the average rating of actors for a given movie.

        :param movie: list[str], A list representing a movie info.
        :param data: list[list], A list of all movie dat.
        :return: float, The average actor rating for the given movie.
        """
        pass

    def sort_film(movie: tuple[str, float]) -> tuple[float, str]:
        """
        Returns a tuple that sorts by descending rating and name alphabetically.

        :param movie: tuple[str, float], A tuple with the movie title and its rating (float).
        :return: tuple[float, str], A tuple with the negative rating (for descending) and title.
        """
        pass

    pass

def write_file(top: list[tuple], file_name: str) -> None:
    """
    function writes the result of top_n function
    into a new file.
    file output example: Intern, 8.5

    :param top: list[tuple], data from top_n function
    :param file_name: str, name of file used for writing information
    :return: new file
    >>> import tempfile
    >>> with tempfile.NamedTemporaryFile(mode = "w",delete=False) as tmp:
    ...         _= tmp.write('')
    >>> write_file([('Dangal', 8.8),\
('Bahubali: The Beginning', 8.3), ('Guardians of the Galaxy', 8.1),\
('Mad Max: Fury Road', 8.1), ('Star Wars: Episode VII - The Force Awakens', 8.1)], tmp.name)
    >>> with open(tmp.name, 'r', encoding ='utf-8') as file:
    ...     print(file.read())
    Dangal, 8.8
    Bahubali: The Beginning, 8.3
    Guardians of the Galaxy, 8.1
    Mad Max: Fury Road, 8.1
    Star Wars: Episode VII - The Force Awakens, 8.1
    """
    pass

if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
