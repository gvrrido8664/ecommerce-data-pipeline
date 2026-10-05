import sys
from pipeline import main
if __name__ == '__main__':
    if '--load-sql' not in sys.argv:
        sys.argv.append('--load-sql')
    main()
