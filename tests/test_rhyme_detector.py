from rhyme_detector import __version__, rhymes


def test_version():
    assert __version__ == "0.1.0"


def test_rhymes_success():
    assert rhymes(
        ["My little horse must think it queer", "To stop without a farmhouse near"]
    )


def test_rhymes_failure():
    assert not rhymes(
        ["My little horse must think it queer", "To stop without a farmhouse purple"]
    )
