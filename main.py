from thespian.actors import ActorSystem
from my_actors import FirstLevelActor

def list_to_dict(list):
    return {key: value for key, value in list}

def get_actors_info():
    file = open("actors.txt", "r")
    lines = file.readlines()
    file.close()

    lines = [line.strip().split(':') for line in lines]
    return list_to_dict(lines)

if __name__ == "__main__":
    asys = ActorSystem("simpleSystemBase")
    fla_dict = {}

    while True:
        actors_info = get_actors_info()
        try:
            for key in actors_info.keys():
                value = actors_info[key]
                if fla_dict.get(key) is None:
                    if value.lower() != "kill":
                        creation_msg = {"name": key, "message": value}
                        fla = asys.createActor(FirstLevelActor)
                        asys.tell(fla, creation_msg)
                        fla_dict[key] = fla
                        print(asys.ask(fla, "hello", timeout=2))
                elif value.lower() == "kill":
                    if asys.ask(fla_dict[key], "alive", timeout=2) == "alive":
                        asys.tell(fla_dict[key], "kill")
                        del fla_dict[key]
            
            for key in fla_dict.keys():
                asys.tell(fla_dict[key], {"data": actors_info[key]})
        except Exception as e:
            pass
        

    # asys.shutdown()