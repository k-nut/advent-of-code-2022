from helpers import get_data


def find_start_of_packet_marker_position(data: str) -> int:
    for i in range(len(data) - 4):
        if len(set(data[i:(i + 4)])) == 4:
            return i + 4


def find_start_of_message_marker_position(data: str) -> int:
    for i in range(len(data) - 14):
        if len(set(data[i:(i + 14)])) == 14:
            return i + 14


def day_6():
    assert find_start_of_packet_marker_position("bvwbjplbgvbhsrlpgdmjqwftvncz") == 5
    assert find_start_of_packet_marker_position("nppdvjthqldpwncqszvftbrmjlhg") == 6
    assert (
        find_start_of_packet_marker_position("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 10
    )
    assert (
        find_start_of_packet_marker_position("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 11
    )

    data = get_data(6)[0]

    print("Part 1: ", find_start_of_packet_marker_position(data))
    print("Part 2: ", find_start_of_message_marker_position(data))


if __name__ == "__main__":
    day_6()
