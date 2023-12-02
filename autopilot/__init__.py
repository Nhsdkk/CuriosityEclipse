from autopilot.src.autopilot import Autopilot

if __name__ == "__main__":
    client1 = Autopilot("addr")
    client2 = Autopilot("addr")

    print(client1 is client2)
