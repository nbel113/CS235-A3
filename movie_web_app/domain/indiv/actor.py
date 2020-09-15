class Actor:
    def __init__(self, actor_full_name: str):
        self.__actor_colleague_list = []
        if actor_full_name == "" or type(actor_full_name) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = actor_full_name.strip()

    @property
    def genre_name(self) -> str:
        return self.__actor_full_name

    def __repr__(self):
        return f"<Actor {self.__actor_full_name}>"

    def __eq__(self, other):
        return self.__actor_full_name == other.__actor_full_name

    def __lt__(self, other):
        if not isinstance(self, Actor) or not isinstance(other, Actor):
            return False
        if self.__actor_full_name < other.__actor_full_name:
            return True
        return False

    def __hash__(self):
        return hash(self.__actor_full_name)

    # if an actor colleague was on the cast for the same movie as this actor, we allow for the colleague to be added to this actor's set of colleagues
    def add_actor_colleague(self, colleague):
        self.__actor_colleague_list.append(colleague)

    # this method checks if a given colleague Actor has worked with the actor at least once in the same movie
    def check_if_this_actor_worked_with(self, colleague):
        return (colleague in self.__actor_colleague_list)
