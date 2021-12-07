import random

# Moves must be defined in the first quadrant (assuming you're sitting at the
# board facing your opponent) to be reflected properly.
STANDARD_MOVE_MAP = {
    'P': {
        'DEFAULT': {
            'patterns': [[[1, 0]]],
            'distance': [1, 1],
            'noncapturing': True
        },
        'FIRST_MOVE': {
            'patterns': [[[1, 0]]],
            'distance': [2, 2],
            'noncapturing': True
        },
        'CAPTURE': {
            'patterns': [[[1, 1]], [[1, -1]]],
            'distance': [1, 1],
        },
    },
    'N': {
        'DEFAULT': {
            'patterns': [[[1, 0], [2, 0], [2, 1]], [[1, 0], [2, 0], [2, -1]]],
            'distance': [3, 3],
            'rotatable': True,
            'jump': True,
        }
    },
    'B': {
        'DEFAULT': {
            'patterns': [[[1, 1]]],
            'distance': 'ANY',
            'rotatable': True,
        }
    },
    'R': {
        'DEFAULT': {
            'patterns': [[[1, 0]]],
            'distance': 'ANY',
            'rotatable': True,
        }
    },
    'Q': {
        'DEFAULT': {
            'patterns': [[[1, 0]], [[1, 1]]],
            'distance': 'ANY',
            'rotatable': True,
        }
    },
    'K': {
        'DEFAULT': {
            'patterns': [[[1, 0]], [[1, 1]]],
            'distance': [1, 1],
            'rotatable': True,
        }
    },
}

TURBO_MOVE_MAP = {
    'P': {
        'DEFAULT': {
            'patterns': [[[1, 0]]],
            'distance': 'ANY',
            'noncapturing': True
        },
        'FIRST_MOVE': {
            'patterns': [[[1, 0]]],
            'distance': 'ANY',
            'noncapturing': True
        },
        'CAPTURE': {
            'patterns': [[[1, 1]], [[1, -1]]],
            'distance': [1, 1],
        },
    },
    'N': {
        'DEFAULT': {
            'patterns': [[[1, 0], [2, 0], [2, 1]], [[1, 0], [2, 0], [2, -1]]],
            'distance': ['MULTIPLESOF', 3],
            'rotatable': True,
            'jump': True,
        }
    },
    'B': {
        'DEFAULT': {
            'patterns': [[[1, 1]]],
            'distance': 'ANY',
            'rotatable': True,
        }
    },
    'R': {
        'DEFAULT': {
            'patterns': [[[1, 0]]],
            'distance': 'ANY',
            'rotatable': True,
        }
    },
    'Q': {
        'DEFAULT': {
            'patterns': [[[1, 0]], [[1, 1]]],
            'distance': 'ANY',
            'rotatable': True,
        }
    },
    'K': {
        'DEFAULT': {
            'patterns': [[[1, 0]], [[1, 1]]],
            'distance': 'ANY',
            'rotatable': True,
        }
    },
}

SLOW_MOVE_MAP = {
    'P': {
        'DEFAULT': {
            'patterns': [[[1, 0]]],
            'distance': [1, 1],
            'noncapturing': True
        },
        'FIRST_MOVE': {
            'patterns': [[[1, 0]]],
            'distance': [1, 1],
            'noncapturing': True
        },
        'CAPTURE': {
            'patterns': [[[1, 1]], [[1, -1]]],
            'distance': [1, 1],
        },
    },
    'N': {
        'DEFAULT': {
            'patterns': [[[1, 0], [2, 0], [2, 1]], [[1, 0], [2, 0], [2, -1]]],
            'distance': [1, 1],
            'rotatable': True,
            'jump': True,
        }
    },
    'B': {
        'DEFAULT': {
            'patterns': [[[1, 1]]],
            'distance': [1, 1],
            'rotatable': True,
        }
    },
    'R': {
        'DEFAULT': {
            'patterns': [[[1, 0]]],
            'distance': [1, 1],
            'rotatable': True,
        }
    },
    'Q': {
        'DEFAULT': {
            'patterns': [[[1, 0]], [[1, 1]]],
            'distance': [1, 1],
            'rotatable': True,
        }
    },
    'K': {
        'DEFAULT': {
            'patterns': [[[1, 0]], [[1, 1]]],
            'distance': [1, 1],
            'rotatable': True,
        }
    },
}

CAPTURES_ONLY_MOVE_MAP = {
    'P': {
        'DEFAULT': {
            'patterns': [[[1, 0]]],
            'distance': [1, 1],
            'noncapturing': True
        },
        'FIRST_MOVE': {
            'patterns': [[[1, 0]]],
            'distance': [1, 1],
            'noncapturing': True
        },
        'CAPTURE': {
            'patterns': [[[1, 1]], [[1, -1]]],
            'distance': [1, 'ANY'],
        },
    },
    'N': {
        'DEFAULT': {
            'patterns': [[[1, 0], [2, 0], [2, 1]], [[1, 0], [2, 0], [2, -1]]],
            'distance': [1, 1],
            'rotatable': True,
            'jump': True,
            'noncapturing': True,
        },
        'CAPTURE': {
            'patterns': [[[1, 0], [2, 0], [2, 1]], [[1, 0], [2, 0], [2, -1]]],
            'distance': ['MULTIPLESOF', 3],
            'jump': True,
            'rotatable': True,
        }
    },
    'B': {
        'DEFAULT': {
            'patterns': [[[1, 1]]],
            'distance': [1, 1],
            'rotatable': True,
            'noncapturing': True,
        },
        'CAPTURE': {
            'patterns': [[[1, 0], [2, 0], [2, 1]], [[1, 0], [2, 0], [2, -1]]],
            'distance': ['MULTIPLESOF', 3],
            'rotatable': True,
        }
    },
    'R': {
        'DEFAULT': {
            'patterns': [[[1, 0]]],
            'distance': [1, 1],
            'rotatable': True,
            'noncapturing': True,
        },
        'CAPTURE': {
            'patterns': [[[1, 0]]],
            'distance': [1, 'ANY'],
            'rotatable': True,
        }
    },
    'Q': {
        'DEFAULT': {
            'patterns': [[[1, 0]], [[1, 1]]],
            'distance': [1, 1],
            'rotatable': True,
            'noncapturing': True,
        },
        'CAPTURE': {
            'patterns': [[[1, 0]], [[1, 1]]],
            'distance': [1, 'ANY'],
            'rotatable': True,
        }
    },
    'K': {
        'DEFAULT': {
            'patterns': [[[1, 0]], [[1, 1]]],
            'distance': [1, 1],
            'rotatable': True,
            'noncapturing': True,
        },
        'CAPTURE': {
            'patterns': [[[1, 0]], [[1, 1]]],
            'distance': [1, 'ANY'],
            'rotatable': True,
        }
    },
}

JUMPY_MOVE_MAP = {
    'P': {
        'DEFAULT': {
            'patterns': [[[1, 0]]],
            'distance': [1, 1],
            'noncapturing': True
        },
        'FIRST_MOVE': {
            'patterns': [[[1, 0]]],
            'distance': [1, 1],
            'noncapturing': True
        },
        'CAPTURE': {
            'patterns': [[[1, 1]], [[1, -1]]],
            'distance': [1, 1],
        },
    },
    'N': {
        'DEFAULT': {
            'patterns': [[[1, 0], [2, 0], [2, 1]], [[1, 0], [2, 0], [2, -1]]],
            'distance': [3, 3],
            'rotatable': True,
            'jump': True,
        }
    },
    'B': {
        'DEFAULT': {
            'patterns': [[[1, 1]]],
            'distance': ['MULTIPLESOF', 2],
            'rotatable': True,
        }
    },
    'R': {
        'DEFAULT': {
            'patterns': [[[1, 0]]],
            'distance': ['MULTIPLESOF', 2],
            'rotatable': True,
        }
    },
    'Q': {
        'DEFAULT': {
            'patterns': [[[1, 0]], [[1, 1]]],
            'distance': ['MULTIPLESOF', 2],
            'rotatable': True,
        }
    },
    'K': {
        'DEFAULT': {
            'patterns': [[[1, 0]], [[1, 1]]],
            'distance': [1, 1],
            'rotatable': True,
        }
    },
}

def gen_chaos_map(height, width):
    return {
        'P': {
            'DEFAULT': {
                'patterns': [[[random.randint(-1 * height, height), random.randint(-1 * width, width)]]],
                'distance': [1, 1],
                'noncapturing': True,
            },
            'FIRST_MOVE': {
                'patterns': [[[random.randint(-1 * height, height), random.randint(-1 * width, width)]]],
                'distance': [2, 2],
                'noncapturing': True
            },
            'CAPTURE': {
                'patterns': [[[random.randint(-1 * height, height), random.randint(-1 * width, width)]], [[random.randint(-1 * height, height), random.randint(-1 * width, width)]]],
                'distance': [1, 1],
            },
        },
        'N': {
            'DEFAULT': {
                'patterns': [[[random.randint(-1 * height, height), random.randint(-1 * width, width)] for _ in range(random.randint(1, 4))]],
                'distance': [3, 3],
                'rotatable': True,
                'jump': True,
            }
        },
        'B': {
            'DEFAULT': {
                'patterns': [[[random.randint(-1 * height, height), random.randint(-1 * width, width)]]],
                'distance': 'ANY',
                'rotatable': True,
            }
        },
        'R': {
            'DEFAULT': {
                'patterns': [[[random.randint(-1 * height, height), random.randint(-1 * width, width)]]],
                'distance': 'ANY',
                'rotatable': True,
            }
        },
        'Q': {
            'DEFAULT': {
                'patterns': [[[random.randint(-1 * height, height), random.randint(-1 * width, width)] for _ in range(3)], [[random.randint(-1 * height, height), random.randint(-1 * width, width)] for _ in range(3)]],
                'distance': 'ANY',
                'rotatable': True,
            }
        },
        'K': {
            'DEFAULT': {
                'patterns': [[[random.randint(-1 * height, height), random.randint(-1 * width, width)] for _ in range(3)], [[random.randint(-1 * height, height), random.randint(-1 * width, width)] for _ in range(3)]],
                'distance': [1, 1],
                'rotatable': True,
            }
        },
    }
