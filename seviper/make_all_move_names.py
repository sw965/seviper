import boa
import seviper.path as path
import seviper.parts as parts

def main():
    assert False, "呼び出さないで"
    boa.write_txt(path.ALL_MOVE_NAMES, "\n".join(parts.ALL_MOVE_NAMES))

if __name__ == "__main__":
    main()
