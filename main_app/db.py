
courses_dict = {
    '1': {
        'title': 'Go',
        'desc': '''Go is a statically typed, compiled programming language
        designed at Google[14] by Robert Griesemer, Rob Pike, and Ken Thompson''',
    },
    '2': {
        'title': 'F#',
        'desc': '''F# (pronounced F sharp) is a functional-first,
        general purpose, strongly typed, multi-paradigm programming language
        that encompasses functional, imperative, and object-oriented programming methods.''',
    },
    '3': {
        'track_ids': ['31', '32', '33'],
        'title': 'Python',
        'desc': '''Python is an interpreted, high-level and general-purpose programming language.
        Created by Guido van Rossum and first released in 1991,
        Python's design philosophy emphasizes code readability with its notable use of significant whitespace.'''
    },
}


tracks_dict = {
    '31': {
        'desc': '''Introduction to the Python programming language.''',
        'title': 'Beginner',
        'lesson_ids': ['311', '312', '313']
    },
    '32': {
        'desc': '''Simple GUI applications.''',
        'title': 'Medium',
        'lesson_ids': ['321', '322', '323']
    },
    '33': {
        'desc': '''Advanced level''',
        'title': 'Hard',
        'lesson_ids': ['331', '332', '333']
    },
}


lessons_dict = {
    '311': {
        'title': 'Arithmetic',
        'task_ids': ['3111', '3112', '3113'],
    },
    '312': {
        'title': 'Types',
    },
    '313': {
        'title': 'Variables',
    },

    '321': {
        'title': 'Tkinter',
    },
    '322': {
        'title': 'Widgets',
    },
    '323': {
        'title': 'Events',
    },

    '331': {
        'title': 'NumPy',
    },
    '332': {
        'title': 'Pandas',
    },
    '333': {
        'title': 'Scikit-learn',
    },
}


tasks_dict = {
    '3111': {
        'type': 'test',
    },
}


tests_dict = {
    '31111': {
        'title': 'Python Arithmetic',
        'desc': '''Checking your knowledge'''
    }
}