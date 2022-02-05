import boa
import path
import base_data

def main():
    boa.write_txt(path.ALL_MOVE_NAMES, "\n".join(base_data.ALL_MOVE_NAMES))

if __name__ == "__main__":
    main()
