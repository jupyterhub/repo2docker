from .app import Repo2Docker

def main():
    f = Repo2Docker()
    f.initialize()
    f.start()

if __name__ == '__main__':
    main()
