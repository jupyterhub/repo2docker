from .app import Repo2Docker

def main():
    f = Repo2Docker()
    f.initialize()
    f.run()

if __name__ == '__main__':
    main()
