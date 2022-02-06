import json
import boa
import seviper.path as path

def main():
    assert False, "呼び出さないで"
    for poke_name in base_data.ALL_POKE_NAMES:
        print(poke_name)
        poke_data = pt_pokedex.parse_poke_data(path.POKETETU_POKEDEX + poke_name + ".txt")
        poketetu_learnset = boa.read_txt(path.POKETETU_LEARNSET + poke_name + ".txt")
        learnset = pt_learnset.parse(poketetu_learnset)
        poke_data["Learnset"] = learnset
        json_data = json.dumps(poke_data, ensure_ascii=False, indent=4)
        boa.write_txt(path.POKEDEX + poke_name + ".json", json_data)

if __name__ == "__main__":
    main()
