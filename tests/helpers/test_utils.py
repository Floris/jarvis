from app.helpers.utils import remove_code_block, remove_whitespace, save_code_to_file


def test_remove_code_block():
    input_str = "This is an example. ```code block``` End of example."
    assert remove_code_block(input_str) == ""

    input_str_no_code_block = "This is an example without a code block."
    assert remove_code_block(input_str_no_code_block) == input_str_no_code_block


def test_remove_whitespace():
    input_str = " Hello, World! "
    expected_output = "Hello,World!"
    assert remove_whitespace(input_str) == expected_output

    input_str_no_whitespace = "Hello,World!"
    assert remove_whitespace(input_str_no_whitespace) == input_str_no_whitespace


def test_save_code_to_file(tmpdir):
    code = "print('Hello, World!')"
    file_path = "test_project"
    file_name = "main.py"

    save_code_to_file(code, str(tmpdir.join(file_path)), file_name)

    saved_file_path = tmpdir.join(file_path, file_name)
    assert saved_file_path.check(file=1)

    with open(saved_file_path) as f:
        content = f.read()
        assert content == code
