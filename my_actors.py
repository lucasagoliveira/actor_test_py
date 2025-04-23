from thespian.actors import Actor, ActorExitRequest, WakeupMessage, ActorTypeDispatcher
from datetime import timedelta

class FirstLevelActor(Actor):
    def __init__(self):
        self.name = "actor"
        self.message = "message"
        self.children = []
        self.stop = False
        
    def receiveMessage(self, msg, sender):
        if self.stop:
            return

        match msg:
            # Initialization case
            case {"name": name, "message": message} if isinstance(msg, dict):
                self._handle_initialization(name, message)
            
            # Data update case
            case {"data": data} if isinstance(msg, dict) and data != self.message:
                self._handle_data_update(data)
            
            # Command cases
            case "kill":
                self._handle_kill()
            case "alive":
                self._handle_alive(sender)
            case "hello":
                self._handle_hello(sender)
            case "address":
                self._handle_address(sender)
            
            # Ignore other cases
            case _:
                pass

    def _handle_initialization(self, name, message):
        self.name = name if name is not None else self.name
        self.message = message if message is not None else self.message
        
        for i in range(2):
            creation_msg = {"name": f"{self.name}_{i}", "message": self.message}
            child = self.createActor(TriggerActor)
            self.send(child, creation_msg)
            self.children.append(child)

    def _handle_data_update(self, data):
        self.message = data
        for child in self.children:
            self.send(child, {"data": self.message})
        print(f"data updated at {self.name}")

    def _handle_kill(self):
        for child in self.children:
            self.send(child, "kill")
        self.children = []
        self.stop = True
        self.send(self.myAddress, ActorExitRequest)

    def _handle_alive(self, sender):
        self.send(sender, "alive")

    def _handle_hello(self, sender):
        self.send(sender, f"Hello from {self.name} with message {self.message}!")

    def _handle_address(self, sender):
        self.send(sender, self.children[0])





class TriggerActor(ActorTypeDispatcher):
    def __init__(self):
        self.name = "trigger"
        self.message = "message"
        self.count = 0
        self.stop = False
        self.wakeup_time = timedelta(seconds=1)

    def receiveMsg_ActorExitRequest(self, msg, sender):
        # Handle actor termination request.
        self.stop = True

    def receiveMsg_WakeupMessage(self, msg, sender):
        # Handle periodic wakeup messages.
        if self.stop:
            return
        
        self._increment_and_log()
        self.wakeupAfter(self.wakeup_time)

    def receiveMsg_dict(self, msg, sender):
        # Handle dictionary-type messages.
        match msg:
            case {"name": name, "message": message}:
                self._handle_initialization(name, message)
            case {"data": data} if data != self.message:
                self._handle_data_update(data)
            case _:
                pass

    def receiveMsg_str(self, msg, sender):
        # Handle string-type messages.
        match msg:
            case "kill":
                self._handle_kill()
            case "hello":
                self._handle_hello(sender)
            case "alive":
                self._handle_alive(sender)
            case _:
                pass

    # Helper methods
    def _increment_and_log(self):
        # Increment counter and log message.
        self.count += 1
        print(f"{self.name} says: {self.message} {self.count}")

    def _handle_initialization(self, name, message):
        # Handle initialization message.
        self.name = name if name is not None else self.name
        self.message = message if message is not None else self.message
        self.wakeupAfter(self.wakeup_time)

    def _handle_data_update(self, data):
        # Handle data update message.
        self.message = data if data is not None else self.message
        print(f"data updated at {self.name}")

    def _handle_kill(self):
        # Handle kill command.
        self.stop = True
        self.send(self.myAddress, ActorExitRequest)

    def _handle_hello(self, sender):
        # Handle hello command.
        self.send(sender, f"Hello from {self.name} with message {self.message}!")

    def _handle_alive(self, sender):
        # Handle alive command.
        self.send(sender, "alive")





### Alternative implementation of TriggerActor using Actor class directly
class TriggerActor_Alt(Actor):
    def __init__(self):
        self.name = "trigger"
        self.message = "message"
        self.count = 0
        self.stop = False
        self.wakeup_time = timedelta(seconds=1)

    def receiveMessage(self, msg, sender):
        # Main message handler that routes to specific handlers.
        if self.stop:
            return
            
        match msg:
            case WakeupMessage():
                self._handle_wakeup()
            case {"name": name, "message": message}:
                self._handle_initialization(name, message)
            case {"data": data} if data != self.message:
                self._handle_data_update(data)
            case "kill":
                self._handle_kill()
            case "hello":
                self._handle_hello(sender)
            case "alive":
                self._handle_alive(sender)
            case _:
                pass

    # Handler methods
    def _handle_wakeup(self):
        # Handle periodic wakeup messages.
        self.count += 1
        print(f"{self.name} says: {self.message} {self.count}")
        self.wakeupAfter(self.wakeup_time)

    def _handle_initialization(self, name, message):
        # Handle initialization message with new name and message.
        self.name = name if name is not None else self.name
        self.message = message if message is not None else self.message
        self.wakeupAfter(self.wakeup_time)

    def _handle_data_update(self, data):
        # Handle data update message.
        self.message = data if data is not None else self.message
        print(f"data updated at {self.name}")

    def _handle_kill(self):
        # Handle kill command.
        self.stop = True
        self.send(self.myAddress, ActorExitRequest)

    def _handle_hello(self, sender):
        # Respond to hello message.
        self.send(sender, f"Hello from {self.name} with message {self.message}!")

    def _handle_alive(self, sender):
        # Respond to alive check.
        self.send(sender, "alive")