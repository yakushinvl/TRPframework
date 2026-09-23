from presentations import (
    check_duration,
    calculate_total_score,
    get_result,
    add_presentation,
    sort_presentations_by_score,
)


def test_check_duration():
    assert check_duration(8, 10) == "В регламенте"
    assert check_duration(12, 10) == "Превышен"


def test_calculate_total_score():
    assert calculate_total_score(4.5, 4.5) == 9.0


def test_get_result():
    assert get_result(9.5) == "1 место"
    assert get_result(8.5) == "2 место"
    assert get_result(7.5) == "3 место"
    assert get_result(6.0) == "Участник"


def test_add_presentation():
    presentations = []
    add_presentation(
        presentations, 1, "Студент", "Группа", "Тема", 8, 4.5, 4.5
    )
    assert len(presentations) == 1
    assert presentations[0]["total_score"] == 9.0


def test_sort_presentations_by_score():
    presentations = [
        {"id": 1, "total_score": 7.0},
        {"id": 2, "total_score": 9.5}
    ]
    sorted_list = sort_presentations_by_score(presentations)
    assert sorted_list[0]["total_score"] == 9.5
