from Position import Position
from Time import Time
from computer.Computer import Computer
from computer.hardware.sound import Microphone, States
from computer.software.sound import SensorController
from computer.software.sound.tdoa import Controller, ControllerState, SensorInfo
from computer.software.sound.duplicates_filter import Filter
from network import Address
from network.hardware import Connection, Adapter
from network.software import Protocol
from sound import Sensor, PropagationEnvironment
from sound.wave import Generator


class F:
    def f(self, name):
        print(str(name))


if __name__ == '__main__':
    time = Time()

    f = F()
    # ss.perceived_something_broadcaster.register(f.f)

    environment = PropagationEnvironment(
        time=time,
        speed_of_sound=0.34029,
        min_sound_power=0.001
    )

    sound_generator_1 = Generator(
        time=time,
        position=Position(7, 0, 0),
        interval=150,
        power=100
    )
    environment.register_sound_source(sound_generator_1)

    sound_generator_2 = Generator(
        time=time,
        position=Position(3, 2, 0),
        interval=150,
        power=200
    )
    environment.register_sound_source(sound_generator_2)

    sound_generator_3 = Generator(
        time=time,
        position=Position(4, 5, 0),
        interval=127,
        power=100
    )
    environment.register_sound_source(sound_generator_3)

    sound_generator_4 = Generator(
        time=time,
        position=Position(2, 3, 0),
        interval=128,
        power=120
    )
    environment.register_sound_source(sound_generator_4)

    sound_sensor_1 = Sensor(
        time=time,
        position=Position(0, 0, 0),
        min_sound_power=0.01
    )

    sound_sensor_2 = Sensor(
        time=time,
        position=Position(0, 10, 0),
        min_sound_power=0.01
    )

    sound_sensor_3 = Sensor(
        time=time,
        position=Position(10, 0, 0),
        min_sound_power=0.01
    )

    sound_sensor_4 = Sensor(
        time=time,
        position=Position(10, 10, 0),
        min_sound_power=0.01
    )

    sound_sensor_5 = Sensor(
        time=time,
        position=Position(5, 5, 0),
        min_sound_power=0.01
    )

    environment.register_sound_sensor(sound_sensor_1)
    environment.register_sound_sensor(sound_sensor_2)
    environment.register_sound_sensor(sound_sensor_3)
    environment.register_sound_sensor(sound_sensor_4)
    environment.register_sound_sensor(sound_sensor_5)

    network_connection_1 = Connection(time, 10, set())

    adapter_1 = Adapter(
        time=time,
        position=Position(0, 0, 0),
        connections={},
        message_statuses={},
        messages_to_transmit={}
    )
    microphone_1 = Microphone(
        time=time,
        position=Position(0, 0, 0),
        sensor=sound_sensor_1,
        state=States.waiting
    )

    computer_1 = Computer(
        hardware={adapter_1, microphone_1},
        software=set()
    )

    adapter_2 = Adapter(
        time=time,
        position=Position(0, 0, 0),
        connections={},
        message_statuses={},
        messages_to_transmit={}
    )

    microphone_2 = Microphone(
        time=time,
        position=Position(0, 10, 0),
        sensor=sound_sensor_2,
        state=States.waiting
    )

    computer_2 = Computer(
        hardware={adapter_2, microphone_2},
        software=set()
    )

    adapter_3 = Adapter(
        time=time,
        position=Position(10, 0, 0),
        connections={},
        message_statuses={},
        messages_to_transmit={}
    )

    microphone_3 = Microphone(
        time=time,
        position=Position(10, 0, 0),
        sensor=sound_sensor_3,
        state=States.waiting
    )

    computer_3 = Computer(
        hardware={adapter_3, microphone_3},
        software=set()
    )

    adapter_4 = Adapter(
        time=time,
        position=Position(10, 10, 0),
        connections={},
        message_statuses={},
        messages_to_transmit={}
    )

    microphone_4 = Microphone(
        time=time,
        position=Position(10, 10, 0),
        sensor=sound_sensor_4,
        state=States.waiting
    )

    computer_4 = Computer(
        hardware={adapter_4, microphone_4},
        software=set()
    )

    adapter_5 = Adapter(
        time=time,
        position=Position(5, 5, 0),
        connections={},
        message_statuses={},
        messages_to_transmit={}
    )

    microphone_5 = Microphone(
        time=time,
        position=Position(5, 5, 0),
        sensor=sound_sensor_5,
        state=States.waiting
    )

    computer_5 = Computer(
        hardware={adapter_5, microphone_5},
        software=set()
    )

    adapter_server = Adapter(
        time=time,
        position=Position(100, 100, 0),
        connections={},
        message_statuses={},
        messages_to_transmit={}
    )

    computer_server = Computer(
        hardware={adapter_server},
        software=set()
    )

    adapter_1.connect(adapter_server, network_connection_1)
    adapter_server.connect(adapter_1, network_connection_1)

    adapter_2.connect(adapter_server, network_connection_1)
    adapter_server.connect(adapter_2, network_connection_1)

    adapter_3.connect(adapter_server, network_connection_1)
    adapter_server.connect(adapter_3, network_connection_1)

    adapter_4.connect(adapter_server, network_connection_1)
    adapter_server.connect(adapter_4, network_connection_1)

    adapter_5.connect(adapter_server, network_connection_1)
    adapter_server.connect(adapter_5, network_connection_1)

    protocol_1 = Protocol(
        time=time,
        route_table={
            'server': adapter_server,
            'sensor_1': adapter_1
        },
        host='sensor_1'
    )
    protocol_1.install(computer_1)

    protocol_2 = Protocol(
        time=time,
        route_table={
            'server': adapter_server,
            'sensor_2': adapter_2
        },
        host='sensor_2'
    )
    protocol_2.install(computer_2)

    protocol_3 = Protocol(
        time=time,
        route_table={
            'server': adapter_server,
            'sensor_3': adapter_3
        },
        host='sensor_3'
    )
    protocol_3.install(computer_3)

    protocol_4 = Protocol(
        time=time,
        route_table={
            'server': adapter_server,
            'sensor_4': adapter_4
        },
        host='sensor_4'
    )
    protocol_4.install(computer_4)

    protocol_5 = Protocol(
        time=time,
        route_table={
            'server': adapter_server,
            'sensor_5': adapter_5
        },
        host='sensor_5'
    )
    protocol_5.install(computer_5)

    protocol_server = Protocol(
        time=time,
        route_table={
            'server': adapter_server
        },
        host='server'
    )
    protocol_server.install(computer_server)

    sensor_controller_1 = SensorController(
        time=time,
        addresses_to_report_about_signals={
            Address(
                host='server',
                port=0
            )
        },
        address=Address(
            host='sensor_1',
            port=0
        )
    )
    sensor_controller_1.install(computer_1)

    sensor_controller_2 = SensorController(
        time=time,
        addresses_to_report_about_signals={
            Address(
                host='server',
                port=0
            )
        },
        address=Address(
            host='sensor_2',
            port=0
        )
    )
    sensor_controller_2.install(computer_2)

    sensor_controller_3 = SensorController(
        time=time,
        addresses_to_report_about_signals={
            Address(
                host='server',
                port=0
            )
        },
        address=Address(
            host='sensor_3',
            port=0
        )
    )
    sensor_controller_3.install(computer_3)

    sensor_controller_4 = SensorController(
        time=time,
        addresses_to_report_about_signals={
            Address(
                host='server',
                port=0
            )
        },
        address=Address(
            host='sensor_4',
            port=0
        )
    )
    sensor_controller_4.install(computer_4)

    sensor_controller_5 = SensorController(
        time=time,
        addresses_to_report_about_signals={
            Address(
                host='server',
                port=0
            )
        },
        address=Address(
            host='sensor_5',
            port=0
        )
    )
    sensor_controller_5.install(computer_5)

    tdoa_controller = Controller(
        time=time,
        address=Address(
            host='server',
            port=0
        ),
        addresses_to_send_reports={
            Address(
                host='server',
                port=2
            )
        },
        sensor_controllers={
            sensor_controller_1.address: SensorInfo(
                position=sound_sensor_1.position,
                last_report=None
            ),
            sensor_controller_2.address: SensorInfo(
                position=sound_sensor_2.position,
                last_report=None
            ),
            sensor_controller_3.address: SensorInfo(
                position=sound_sensor_3.position,
                last_report=None
            ),
            sensor_controller_4.address: SensorInfo(
                position=sound_sensor_4.position,
                last_report=None
            ),
            sensor_controller_5.address: SensorInfo(
                position=sound_sensor_5.position,
                last_report=None
            ),
        },
        state=ControllerState.waiting,
        speed_of_sound=environment.speed_of_sound,
        active_timer=None
    )
    tdoa_controller.install(computer_server)

    duplicates_filter = Filter(
        time=time,
        address=Address(
            host='server',
            port=2
        ),
        addresses_to_send_reports=set(),
        time_window=500,
        max_deviation_in_space=1,
        filtrations=set()
    )
    # duplicates_filter.install(computer_server)

    # protocol_2.port_broadcaster(0).register(f.f)

    for i in range(0, 2000):
        time.to_next_tick()

    print('Система распознала событий: {0}'.format(Controller.recognized_events))
    print('Всего событий: {0}'.format(Generator.events))

    print(i)
