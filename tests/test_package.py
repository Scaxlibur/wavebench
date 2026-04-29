from wavebench.data.package import safe_label

def test_safe_label_keeps_simple_names():
    assert safe_label("ch1") == "ch1"

def test_safe_label_replaces_spaces():
    assert safe_label("my capture") == "my_capture"
