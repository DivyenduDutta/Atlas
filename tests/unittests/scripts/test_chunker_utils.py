import pytest

from atlas.utils.chunker_utils import slugify


@pytest.mark.unittest
@pytest.mark.runonci
def test_slugify():
    """
    Test the slugify function to ensure it converts strings to URL-friendly slugs.
    """
    assert slugify("Hello World!") == "hello_world"
    assert slugify("This is a Test.") == "this_is_a_test"
    assert slugify("Special #$& Characters") == "special_characters"
    assert slugify("  Leading and Trailing  ") == "leading_and_trailing"
    assert slugify("Multiple   Spaces") == "multiple_spaces"
