import matplotlib.pyplot as plt
import numpy
import numpy as np

from Position import Position
from Time import Time
from computer.Computer import Computer
from computer.hardware.sound import Microphone, States
from computer.software.sound import SensorController
from computer.software.sound.duplicates_filter import Filter
from computer.software.sound.tdoa import Controller, SensorInfo
from network import Address
from network.hardware import Connection, Adapter
from network.software import Protocol
from sound import Sensor, PropagationEnvironment
from sound.wave import Generator


class F:
    def f(self, name):
        print(str(name))


count_of_generators = 1
max_space_error = 0.5
max_variance = 5000

speed = 10 / 5000

move_first_generator = True


def draw_fixed_case():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4))
    fig.canvas.set_window_title('Усі реакції системи')
    # ax.plot(10 * np.random.randn(100), 10 * np.random.randn(100), 'o')
    ax1.scatter(
        x=[p['position'].x for p in Controller.source_positions],
        y=[p['position'].y for p in Controller.source_positions],
        label='Розраховані позиції джерел'
    )
    ax1.scatter(
        x=[p.position.x for p in generators],
        y=[p.position.y for p in generators],
        s=20,
        c='r',
        label='Істинні позиції джерел'
    )
    ax1.scatter(
        x=[s.position.x for s in sensors],
        y=[s.position.y for s in sensors],
        s=20,
        c='g',
        label='Позиції сенсорів'
    )
    ax1.set_xlabel('Координата X')
    ax1.set_ylabel('Координата Y')
    ax1.legend()
    ax1.set_title('Усі реакції системи')
    # plt.show()
    true_events = []
    for recognized_event in Controller.source_positions:

        for generator in generators:
            x_error = (recognized_event['position'].x - generator.position.x)
            y_error = (recognized_event['position'].y - generator.position.y)
            if abs(x_error) < max_space_error and abs(y_error) < max_space_error:
                true_events.append(recognized_event)
                break
    print('Правильно распознано событий: {0}'.format(len(true_events)))
    # fig, ax1 = plt.subplots(1, 2)
    # fig.canvas.set_window_title('Реакції з точністю до {0} одиниць довжини'.format(max_space_error))
    # ax.plot(10 * np.random.randn(100), 10 * np.random.randn(100), 'o')
    ax2.scatter(
        x=[p['position'].x for p in true_events],
        y=[p['position'].y for p in true_events],
        label='Розраховані позиції джерел'
    )
    ax2.scatter(
        x=[p.position.x for p in generators],
        y=[p.position.y for p in generators],
        s=20,
        c='r',
        label='Істинні позиції джерел'
    )
    ax2.scatter(
        x=[s.position.x for s in sensors],
        y=[s.position.y for s in sensors],
        s=20,
        c='g',
        label='Позиції сенсорів'
    )
    ax2.legend()
    ax2.set_title('Реакції системи з точністю до {0} одиниць довжини'.format(max_space_error))
    ax2.set_xlabel('Координата X')
    ax2.set_ylabel('Координата Y')
    plt.show()


def draw_moving_case():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4))
    fig.canvas.set_window_title('Усі реакції системи')
    # ax.plot(10 * np.random.randn(100), 10 * np.random.randn(100), 'o')
    ax1.scatter(
        x=[p['position'].x for p in Controller.source_positions],
        y=[p['position'].y for p in Controller.source_positions],
        label='Розраховані позиції джерела'
    )
    ax1.plot(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        color='r',
        linestyle='-',
        label='Істинна траекторія'
    )
    ax1.scatter(
        x=[s.position.x for s in sensors],
        y=[s.position.y for s in sensors],
        s=20,
        c='g',
        label='Позиції сенсорів'
    )
    ax1.set_xlabel('Координата X')
    ax1.set_ylabel('Координата Y')
    ax1.legend()
    ax1.set_title('Усі реакції системи')
    # plt.show()
    true_events = []
    for recognized_event in Controller.source_positions:

        for generator in generators:
            d = numpy.linalg.norm(
                numpy.cross(
                    [10, 10],
                    [-recognized_event['position'].x, -recognized_event['position'].y]
                )
            ) / numpy.linalg.norm(
                [10, 10]
            )
            if abs(d) < max_space_error:
                true_events.append(recognized_event)
                break
    ax2.scatter(
        x=[p['position'].x for p in true_events],
        y=[p['position'].y for p in true_events],
        label='Розраховані позиції джерел'
    )
    ax2.plot(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        color='r',
        linestyle='-',
        label='Істинна траекторія'
    )
    ax2.scatter(
        x=[s.position.x for s in sensors],
        y=[s.position.y for s in sensors],
        s=20,
        c='g',
        label='Позиції сенсорів'
    )
    ax2.set_xlabel('Координата X')
    ax2.set_ylabel('Координата Y')
    ax2.legend()
    ax2.set_title('Реакції системи з точністю до {0} одиниць довжини'.format(max_space_error))
    print('Правильно распознано событий: {0}'.format(len(true_events)))
    plt.show()


if __name__ == '__main__':
    time = Time()

    f = F()
    # ss.perceived_something_broadcaster.register(f.f)

    environment = PropagationEnvironment(
        time=time,
        speed_of_sound=0.34029,
        min_sound_power=0.001
    )
    np.random.seed(19680801)
    generators = [
        Generator(
            time=time,
            position=Position(
                x=np.random.random() * 7,
                y=np.random.random() * 7,
                z=0
            ),
            interval=np.random.randint(1, 10),
            power=np.random.randint(100, 200),
            count_of_events_to_generate=1500
        )
        for i in range(0, count_of_generators)
    ]

    for g in generators:
        environment.register_sound_source(g)

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

    sensors = {sound_sensor_1, sound_sensor_2, sound_sensor_3, sound_sensor_3, sound_sensor_4, sound_sensor_5}

    for s in sensors:
        environment.register_sound_sensor(s)

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
        speed_of_sound=environment.speed_of_sound,
        max_variance=max_variance
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

    if move_first_generator:
        generators[0].position.x = 0
        generators[0].position.y = 0

    for i in range(0, 5000):
        if move_first_generator:
            generators[0].position.x += speed
            generators[0].position.y += speed
        time.to_next_tick()

    print('Система распознала событий: {0}'.format(Controller.count_of_recognized_events))
    print('Всего событий: {0}'.format(len(Generator.events)))

    if move_first_generator:
        draw_moving_case()
    else:
        draw_fixed_case()
